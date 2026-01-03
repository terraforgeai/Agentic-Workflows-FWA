#!/usr/bin/env python3
"""
Create Manufacturing Order - Deterministic Odoo Operation

Purpose: Create a new Manufacturing Order in Odoo with BOM and components
Input: Product info, quantity, optional BOM and scheduling
Output: Created MO ID, reference, component availability

Related Directive: directives/create_manufacturing_order_directive.md
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from odoo_connect import OdooConnection, OdooConnectionError
from error_handler import handle_error, log_operation, OperationLogger
from field_mappings import MANUFACTURING_ORDER_FIELDS, FWA_FABRIC_CONSUMPTION

# Setup logging
logger = logging.getLogger(__name__)


def validate_inputs(params: Dict[str, Any]) -> None:
    """
    Validate all required inputs.

    Args:
        params: Input parameters

    Raises:
        ValueError: If validation fails
    """
    # Must have product identifier
    if not params.get('product_name') and not params.get('product_id'):
        raise ValueError("Either 'product_name' or 'product_id' is required")

    # Must have quantity
    quantity = params.get('quantity')
    if quantity is None:
        raise ValueError("'quantity' is required")
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError("'quantity' must be a positive number")


def lookup_product(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find product in Odoo.

    Args:
        odoo: Odoo connection
        params: Input parameters with product_name or product_id

    Returns:
        Product data dict

    Raises:
        ValueError: If product not found or not manufacturable
    """
    if params.get('product_id'):
        products = odoo.read('product.product', [params['product_id']],
                             ['name', 'type', 'uom_id'])
        if not products:
            raise ValueError(f"Product with ID {params['product_id']} not found")
        product = products[0]
    else:
        name = params['product_name']
        domain = [('name', 'ilike', name), ('type', '=', 'product')]
        products = odoo.search_read('product.product', domain,
                                     ['name', 'type', 'uom_id'], limit=5)
        if not products:
            raise ValueError(f"Product '{name}' not found or not a storable product")

        if len(products) > 1:
            exact = [p for p in products if p['name'].lower() == name.lower()]
            if exact:
                product = exact[0]
            else:
                logger.warning(f"Multiple products match '{name}'. Using: {products[0]['name']}")
                product = products[0]
        else:
            product = products[0]

    # Verify it's a storable product
    if product['type'] != 'product':
        raise ValueError(f"Product '{product['name']}' is type '{product['type']}', not 'product' (storable)")

    return product


def lookup_bom(odoo: OdooConnection, product_id: int, bom_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Find BOM for product.

    Args:
        odoo: Odoo connection
        product_id: Product ID
        bom_id: Optional specific BOM ID

    Returns:
        BOM data dict

    Raises:
        ValueError: If BOM not found
    """
    if bom_id:
        boms = odoo.read('mrp.bom', [bom_id], ['product_tmpl_id', 'product_id', 'code', 'bom_line_ids'])
        if not boms:
            raise ValueError(f"BOM with ID {bom_id} not found")
        return boms[0]

    # Find BOM for product
    # First try product-specific BOM
    domain = [('product_id', '=', product_id), ('active', '=', True)]
    boms = odoo.search_read('mrp.bom', domain,
                            ['product_tmpl_id', 'product_id', 'code', 'bom_line_ids'],
                            order='sequence', limit=1)

    if not boms:
        # Try template-level BOM
        product = odoo.read('product.product', [product_id], ['product_tmpl_id'])[0]
        template_id = product['product_tmpl_id'][0]

        domain = [('product_tmpl_id', '=', template_id), ('product_id', '=', False), ('active', '=', True)]
        boms = odoo.search_read('mrp.bom', domain,
                                ['product_tmpl_id', 'product_id', 'code', 'bom_line_ids'],
                                order='sequence', limit=1)

    if not boms:
        raise ValueError(f"No Bill of Materials found for product ID {product_id}. Create a BOM first.")

    return boms[0]


def get_bom_components(odoo: OdooConnection, bom: Dict[str, Any], quantity: float) -> List[Dict[str, Any]]:
    """
    Get BOM components with availability info.

    Args:
        odoo: Odoo connection
        bom: BOM data dict
        quantity: Quantity to manufacture

    Returns:
        List of component dicts with availability
    """
    if not bom.get('bom_line_ids'):
        return []

    # Read BOM lines
    lines = odoo.read('mrp.bom.line', bom['bom_line_ids'],
                      ['product_id', 'product_qty', 'product_uom_id'])

    components = []
    for line in lines:
        product_id = line['product_id'][0]
        product_name = line['product_id'][1]
        qty_per_unit = line['product_qty']
        qty_required = qty_per_unit * quantity

        # Check stock availability
        stock_domain = [('product_id', '=', product_id), ('location_id.usage', '=', 'internal')]
        stock = odoo.search_read('stock.quant', stock_domain,
                                  ['quantity', 'reserved_quantity'])

        total_qty = sum(s['quantity'] for s in stock)
        reserved_qty = sum(s['reserved_quantity'] for s in stock)
        available_qty = total_qty - reserved_qty

        status = 'available' if available_qty >= qty_required else 'shortage'
        shortage = max(0, qty_required - available_qty)

        components.append({
            'product_id': product_id,
            'product': product_name,
            'qty_per_unit': qty_per_unit,
            'qty_required': round(qty_required, 2),
            'qty_available': round(available_qty, 2),
            'status': status,
            'shortage': round(shortage, 2) if shortage > 0 else None,
            'uom': line['product_uom_id'][1] if line.get('product_uom_id') else 'Units'
        })

    return components


def create_manufacturing_order(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a manufacturing order in Odoo.

    Args:
        odoo: Odoo connection
        params: Validated input parameters

    Returns:
        Result dict with MO details
    """
    # Lookup product
    product = lookup_product(odoo, params)
    product_id = product['id']
    quantity = params['quantity']

    # Lookup BOM
    bom = lookup_bom(odoo, product_id, params.get('bom_id'))

    # Get components with availability
    components = get_bom_components(odoo, bom, quantity)

    # Check for shortages
    shortages = [c for c in components if c['status'] == 'shortage']

    # Prepare MO values
    mo_vals = {
        'product_id': product_id,
        'product_qty': quantity,
        'bom_id': bom['id'],
    }

    # Optional fields
    if params.get('scheduled_date'):
        mo_vals['date_planned_start'] = params['scheduled_date']
    if params.get('origin'):
        mo_vals['origin'] = params['origin']

    # Create MO
    mo_id = odoo.create('mrp.production', mo_vals)

    # Get MO reference
    mo_data = odoo.read('mrp.production', [mo_id], ['name', 'state'])[0]

    # Optionally confirm
    if params.get('auto_confirm', False) and not shortages:
        odoo.execute('mrp.production', 'action_confirm', [mo_id])
        mo_data = odoo.read('mrp.production', [mo_id], ['state'])[0]

    result = {
        'mo_id': mo_id,
        'mo_ref': mo_data['name'],
        'product': product['name'],
        'product_id': product_id,
        'quantity': quantity,
        'bom_id': bom['id'],
        'bom_code': bom.get('code') or f"BOM/{product['name']}",
        'components': components,
        'state': mo_data['state'],
        'has_shortages': len(shortages) > 0,
    }

    if shortages:
        result['shortages'] = shortages
        result['warning'] = f"Component shortages detected: {len(shortages)} items"

    return result


def main(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function.

    Args:
        input_params: Dictionary with required parameters

    Returns:
        Dictionary with operation result (success/failure, data, messages)
    """
    with OperationLogger('create_manufacturing_order', input_params):
        try:
            # 1. Validate inputs
            validate_inputs(input_params)

            # 2. Connect to Odoo
            odoo = OdooConnection()

            # 3. Execute operation
            result = create_manufacturing_order(odoo, input_params)

            message = f"Manufacturing Order {result['mo_ref']} created for {result['quantity']} x {result['product']}"
            if result.get('has_shortages'):
                message += f" (Warning: {len(result['shortages'])} component shortages)"

            return {
                'status': 'success',
                'data': result,
                'message': message
            }

        except ValueError as e:
            error_response = handle_error(e, {'operation': 'create_manufacturing_order', 'params': input_params})
            return error_response

        except OdooConnectionError as e:
            error_response = handle_error(e, {'operation': 'create_manufacturing_order'})
            return error_response

        except Exception as e:
            error_response = handle_error(e, {'operation': 'create_manufacturing_order', 'params': input_params})
            return error_response


if __name__ == '__main__':
    # CLI interface
    import argparse

    parser = argparse.ArgumentParser(description='Create Manufacturing Order in Odoo')
    parser.add_argument('--product', type=str, help='Product name')
    parser.add_argument('--product-id', type=int, help='Product ID')
    parser.add_argument('--quantity', type=float, required=True, help='Quantity to manufacture')
    parser.add_argument('--bom-id', type=int, help='Specific BOM ID (optional)')
    parser.add_argument('--origin', type=str, help='Source document reference')
    parser.add_argument('--date', type=str, help='Scheduled start date (YYYY-MM-DD)')
    parser.add_argument('--confirm', action='store_true', help='Auto-confirm the order')
    parser.add_argument('--json', type=str, help='JSON input file or string')

    args = parser.parse_args()

    # Build input from args or JSON
    if args.json:
        if os.path.isfile(args.json):
            with open(args.json) as f:
                test_input = json.load(f)
        else:
            test_input = json.loads(args.json)
    else:
        test_input = {
            'product_name': args.product,
            'product_id': args.product_id,
            'quantity': args.quantity,
            'bom_id': args.bom_id,
            'origin': args.origin,
            'scheduled_date': args.date,
            'auto_confirm': args.confirm,
        }

    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
