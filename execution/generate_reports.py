#!/usr/bin/env python3
"""
Generate Reports - Deterministic Odoo Operation

Purpose: Generate various reports from Odoo data
Input: Report type, filters, date ranges
Output: Formatted report data

Related Directive: directives/generate_reports_directive.md
"""

import os
import sys
import json
import csv
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from odoo_connect import OdooConnection, OdooConnectionError
from error_handler import handle_error, log_operation, OperationLogger

# Setup logging
logger = logging.getLogger(__name__)


REPORT_TYPES = ['sales', 'inventory', 'manufacturing', 'purchase', 'bom']


def validate_inputs(params: Dict[str, Any]) -> None:
    """Validate input parameters."""
    report_type = params.get('report_type', '').lower()
    if report_type not in REPORT_TYPES:
        raise ValueError(f"Invalid report_type. Must be one of: {REPORT_TYPES}")


def generate_sales_report(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate sales report."""
    # Build domain
    domain = []

    if params.get('date_from'):
        domain.append(('date_order', '>=', params['date_from']))
    if params.get('date_to'):
        domain.append(('date_order', '<=', params['date_to']))
    if params.get('customer_id'):
        domain.append(('partner_id', '=', params['customer_id']))
    if params.get('state'):
        domain.append(('state', '=', params['state']))
    else:
        domain.append(('state', 'in', ['sale', 'done']))

    # Fetch orders
    orders = odoo.search_read('sale.order', domain,
                               ['name', 'date_order', 'partner_id', 'amount_total', 'state', 'order_line'],
                               order='date_order desc')

    # Calculate summary
    total_revenue = sum(o['amount_total'] for o in orders)

    # Format data
    data = []
    for order in orders:
        # Get order lines summary
        if order.get('order_line'):
            lines = odoo.read('sale.order.line', order['order_line'][:5],
                              ['product_id', 'product_uom_qty'])
            products = [f"{l['product_id'][1]} x {int(l['product_uom_qty'])}"
                        for l in lines if l.get('product_id')]
        else:
            products = []

        data.append({
            'order_ref': order['name'],
            'date': order['date_order'][:10] if order.get('date_order') else None,
            'customer': order['partner_id'][1] if order.get('partner_id') else 'Unknown',
            'products': products,
            'total': order['amount_total'],
            'state': order['state']
        })

    return {
        'report': 'sales',
        'period': f"{params.get('date_from', 'all')} to {params.get('date_to', 'now')}",
        'summary': {
            'total_orders': len(orders),
            'total_revenue': round(total_revenue, 2),
            'average_order_value': round(total_revenue / len(orders), 2) if orders else 0
        },
        'data': data
    }


def generate_inventory_report(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate inventory report."""
    # Build domain for stock quants
    domain = [('location_id.usage', '=', 'internal')]

    if params.get('location'):
        domain.append(('location_id.complete_name', 'ilike', params['location']))

    # Fetch quants
    quants = odoo.search_read('stock.quant', domain,
                               ['product_id', 'location_id', 'quantity', 'reserved_quantity'])

    # Aggregate by product-location
    inventory = {}
    for quant in quants:
        key = (quant['product_id'][0], quant['location_id'][0])
        if key not in inventory:
            inventory[key] = {
                'product_id': quant['product_id'][0],
                'product': quant['product_id'][1],
                'location_id': quant['location_id'][0],
                'location': quant['location_id'][1],
                'on_hand': 0,
                'reserved': 0,
            }
        inventory[key]['on_hand'] += quant['quantity']
        inventory[key]['reserved'] += quant.get('reserved_quantity', 0)

    # Calculate available and filter
    data = []
    low_stock_count = 0
    threshold = params.get('threshold', 50)

    for item in inventory.values():
        item['available'] = item['on_hand'] - item['reserved']

        if params.get('low_stock_only') and item['available'] >= threshold:
            continue

        if item['available'] < threshold:
            low_stock_count += 1

        # Get product cost if requested
        if params.get('include_value'):
            product = odoo.read('product.product', [item['product_id']], ['standard_price'])
            unit_cost = product[0]['standard_price'] if product else 0
            item['unit_cost'] = round(unit_cost, 2)
            item['total_value'] = round(item['on_hand'] * unit_cost, 2)

        data.append({
            'product': item['product'],
            'location': item['location'],
            'on_hand': round(item['on_hand'], 2),
            'reserved': round(item['reserved'], 2),
            'available': round(item['available'], 2),
            **({k: item[k] for k in ['unit_cost', 'total_value'] if k in item})
        })

    total_value = sum(d.get('total_value', 0) for d in data)

    return {
        'report': 'inventory',
        'location': params.get('location', 'All'),
        'summary': {
            'total_products': len(data),
            'total_value': round(total_value, 2) if params.get('include_value') else None,
            'low_stock_items': low_stock_count
        },
        'data': sorted(data, key=lambda x: x['available'])
    }


def generate_manufacturing_report(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate manufacturing report."""
    # Build domain
    domain = []

    if params.get('date_from'):
        domain.append(('date_planned_start', '>=', params['date_from']))
    if params.get('date_to'):
        domain.append(('date_planned_start', '<=', params['date_to']))
    if params.get('product_id'):
        domain.append(('product_id', '=', params['product_id']))
    if params.get('state'):
        domain.append(('state', '=', params['state']))

    # Fetch MOs
    mos = odoo.search_read('mrp.production', domain,
                            ['name', 'product_id', 'product_qty', 'state',
                             'date_planned_start', 'origin'],
                            order='date_planned_start')

    # Count by state
    state_counts = {}
    total_produced = 0
    for mo in mos:
        state = mo['state']
        state_counts[state] = state_counts.get(state, 0) + 1
        if state == 'done':
            total_produced += mo['product_qty']

    # Format data
    data = []
    for mo in mos:
        data.append({
            'mo_ref': mo['name'],
            'product': mo['product_id'][1] if mo.get('product_id') else 'Unknown',
            'quantity': mo['product_qty'],
            'state': mo['state'],
            'scheduled_start': mo['date_planned_start'][:10] if mo.get('date_planned_start') else None,
            'origin': mo.get('origin')
        })

    return {
        'report': 'manufacturing',
        'period': f"{params.get('date_from', 'all')} to {params.get('date_to', 'now')}",
        'summary': {
            'total_orders': len(mos),
            'in_progress': state_counts.get('progress', 0),
            'completed': state_counts.get('done', 0),
            'cancelled': state_counts.get('cancel', 0),
            'total_produced': int(total_produced)
        },
        'data': data
    }


def generate_purchase_report(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate purchase report."""
    # Build domain
    domain = []

    if params.get('date_from'):
        domain.append(('date_order', '>=', params['date_from']))
    if params.get('date_to'):
        domain.append(('date_order', '<=', params['date_to']))
    if params.get('vendor_id'):
        domain.append(('partner_id', '=', params['vendor_id']))
    if params.get('state'):
        domain.append(('state', '=', params['state']))
    else:
        domain.append(('state', 'in', ['purchase', 'done']))

    # Fetch POs
    pos = odoo.search_read('purchase.order', domain,
                            ['name', 'date_order', 'partner_id', 'amount_total',
                             'state', 'date_planned', 'order_line'],
                            order='date_order desc')

    total_spent = sum(p['amount_total'] for p in pos)

    # Format data
    data = []
    for po in pos:
        # Get order lines summary
        if po.get('order_line'):
            lines = odoo.read('purchase.order.line', po['order_line'][:5],
                              ['product_id', 'product_qty'])
            products = [f"{l['product_id'][1]} x {int(l['product_qty'])}"
                        for l in lines if l.get('product_id')]
        else:
            products = []

        data.append({
            'po_ref': po['name'],
            'date': po['date_order'][:10] if po.get('date_order') else None,
            'vendor': po['partner_id'][1] if po.get('partner_id') else 'Unknown',
            'products': products,
            'total': po['amount_total'],
            'state': po['state'],
            'expected_date': po['date_planned'][:10] if po.get('date_planned') else None
        })

    return {
        'report': 'purchase',
        'period': f"{params.get('date_from', 'all')} to {params.get('date_to', 'now')}",
        'summary': {
            'total_orders': len(pos),
            'total_spent': round(total_spent, 2),
        },
        'data': data
    }


def generate_bom_report(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate BOM report."""
    if params.get('bom_id'):
        bom_ids = [params['bom_id']]
    elif params.get('product_id'):
        product = odoo.read('product.product', [params['product_id']], ['product_tmpl_id'])[0]
        template_id = product['product_tmpl_id'][0]
        bom_ids = odoo.search('mrp.bom', [('product_tmpl_id', '=', template_id)], limit=1)
    else:
        raise ValueError("Either 'bom_id' or 'product_id' is required for BOM report")

    if not bom_ids:
        raise ValueError("No BOM found for specified product")

    bom = odoo.read('mrp.bom', bom_ids, ['product_tmpl_id', 'product_id', 'code', 'bom_line_ids'])[0]

    # Get product name
    if bom.get('product_id'):
        product_name = bom['product_id'][1]
    else:
        template = odoo.read('product.template', [bom['product_tmpl_id'][0]], ['name'])[0]
        product_name = template['name']

    # Get BOM lines
    components = []
    total_cost = 0

    if bom.get('bom_line_ids'):
        lines = odoo.read('mrp.bom.line', bom['bom_line_ids'],
                          ['product_id', 'product_qty', 'product_uom_id'])

        for line in lines:
            product = odoo.read('product.product', [line['product_id'][0]],
                                ['name', 'standard_price'])[0]
            qty = line['product_qty']
            cost = product['standard_price']
            line_cost = qty * cost

            total_cost += line_cost

            components.append({
                'product': product['name'],
                'product_id': line['product_id'][0],
                'quantity': qty,
                'uom': line['product_uom_id'][1] if line.get('product_uom_id') else 'Units',
                'unit_cost': round(cost, 2) if params.get('include_costs') else None,
                'total_cost': round(line_cost, 2) if params.get('include_costs') else None
            })

    return {
        'report': 'bom',
        'product': product_name,
        'bom_ref': bom.get('code') or f"BOM/{product_name}",
        'summary': {
            'total_components': len(components),
            'total_cost': round(total_cost, 2) if params.get('include_costs') else None
        },
        'components': components
    }


def export_to_csv(data: Dict[str, Any], output_path: str) -> str:
    """Export report data to CSV."""
    if not data.get('data'):
        return None

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data['data'][0].keys())
        writer.writeheader()
        writer.writerows(data['data'])

    return output_path


def main(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """Main execution function."""
    with OperationLogger('generate_reports', input_params):
        try:
            validate_inputs(input_params)
            odoo = OdooConnection()

            report_type = input_params.get('report_type', '').lower()

            # Generate appropriate report
            if report_type == 'sales':
                result = generate_sales_report(odoo, input_params)
            elif report_type == 'inventory':
                result = generate_inventory_report(odoo, input_params)
            elif report_type == 'manufacturing':
                result = generate_manufacturing_report(odoo, input_params)
            elif report_type == 'purchase':
                result = generate_purchase_report(odoo, input_params)
            elif report_type == 'bom':
                result = generate_bom_report(odoo, input_params)
            else:
                raise ValueError(f"Unknown report type: {report_type}")

            # Export to CSV if requested
            if input_params.get('output_format') == 'csv':
                output_dir = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'odoo_exports')
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(output_dir, f"{report_type}_report_{timestamp}.csv")
                export_to_csv(result, output_path)
                result['csv_file'] = output_path

            return {
                'status': 'success',
                'data': result,
                'message': f"{report_type.title()} report generated successfully"
            }

        except ValueError as e:
            return handle_error(e, {'operation': 'generate_reports'})
        except OdooConnectionError as e:
            return handle_error(e, {'operation': 'generate_reports'})
        except Exception as e:
            return handle_error(e, {'operation': 'generate_reports'})


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate Odoo Reports')
    parser.add_argument('--type', type=str, required=True, choices=REPORT_TYPES, help='Report type')
    parser.add_argument('--from', dest='date_from', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to', dest='date_to', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--product-id', type=int, help='Filter by product ID')
    parser.add_argument('--location', type=str, help='Filter by location')
    parser.add_argument('--low-stock', action='store_true', help='Show only low stock items')
    parser.add_argument('--include-costs', action='store_true', help='Include cost information')
    parser.add_argument('--csv', action='store_true', help='Export to CSV')

    args = parser.parse_args()

    test_input = {
        'report_type': args.type,
        'date_from': args.date_from,
        'date_to': args.date_to,
        'product_id': args.product_id,
        'location': args.location,
        'low_stock_only': args.low_stock,
        'include_costs': args.include_costs,
        'output_format': 'csv' if args.csv else 'json'
    }

    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
