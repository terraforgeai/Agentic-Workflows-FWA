#!/usr/bin/env python3
"""
Process Purchase Order - Deterministic Odoo Operation

Purpose: Create a new Purchase Order in Odoo for ordering materials/goods
Input: Vendor info, product lines with quantities and prices
Output: Created PO ID, reference, and order details

Related Directive: directives/process_purchase_order_directive.md
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
from field_mappings import PURCHASE_ORDER_FIELDS

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
    # Must have vendor identifier
    if not params.get('vendor_name') and not params.get('vendor_id'):
        raise ValueError("Either 'vendor_name' or 'vendor_id' is required")

    # Must have at least one product
    products = params.get('products', [])
    if not products:
        raise ValueError("At least one product is required in 'products' list")

    # Validate each product line
    for i, product in enumerate(products):
        if not product.get('product_name') and not product.get('product_id'):
            raise ValueError(f"Product {i+1}: Either 'product_name' or 'product_id' is required")

        quantity = product.get('quantity')
        if quantity is None:
            raise ValueError(f"Product {i+1}: 'quantity' is required")
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            raise ValueError(f"Product {i+1}: 'quantity' must be a positive number")


def lookup_vendor(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find vendor in Odoo.

    Args:
        odoo: Odoo connection
        params: Input parameters with vendor_name or vendor_id

    Returns:
        Vendor data dict

    Raises:
        ValueError: If vendor not found
    """
    if params.get('vendor_id'):
        vendors = odoo.read('res.partner', [params['vendor_id']],
                            ['name', 'email', 'supplier_rank', 'property_purchase_currency_id'])
        if not vendors:
            raise ValueError(f"Vendor with ID {params['vendor_id']} not found")
        return vendors[0]

    # Search by name
    name = params['vendor_name']
    domain = [('name', 'ilike', name), ('supplier_rank', '>', 0)]
    vendors = odoo.search_read('res.partner', domain,
                                ['name', 'email', 'supplier_rank', 'property_purchase_currency_id'],
                                limit=5)

    if not vendors:
        domain = [('name', 'ilike', f'%{name}%')]
        all_partners = odoo.search_read('res.partner', domain, ['name'], limit=5)
        suggestions = [p['name'] for p in all_partners] if all_partners else []
        raise ValueError(f"Vendor '{name}' not found. Similar: {suggestions}")

    if len(vendors) > 1:
        logger.warning(f"Multiple vendors match '{name}'. Using: {vendors[0]['name']}")

    return vendors[0]


def lookup_product(odoo: OdooConnection, product_info: Dict[str, Any],
                   vendor_id: int) -> Dict[str, Any]:
    """
    Find product in Odoo with supplier pricing.

    Args:
        odoo: Odoo connection
        product_info: Product dict with product_name or product_id
        vendor_id: Vendor ID for supplier price lookup

    Returns:
        Product data dict with pricing

    Raises:
        ValueError: If product not found
    """
    if product_info.get('product_id'):
        products = odoo.read('product.product', [product_info['product_id']],
                             ['name', 'standard_price', 'uom_po_id', 'purchase_ok'])
        if not products:
            raise ValueError(f"Product with ID {product_info['product_id']} not found")
        if not products[0].get('purchase_ok'):
            raise ValueError(f"Product '{products[0]['name']}' is not available for purchase")
        product = products[0]
    else:
        name = product_info['product_name']
        domain = [('name', 'ilike', name), ('purchase_ok', '=', True)]
        products = odoo.search_read('product.product', domain,
                                     ['name', 'standard_price', 'uom_po_id'], limit=5)
        if not products:
            raise ValueError(f"Product '{name}' not found or not available for purchase")

        if len(products) > 1:
            exact = [p for p in products if p['name'].lower() == name.lower()]
            product = exact[0] if exact else products[0]
        else:
            product = products[0]

    # Try to get supplier price
    supplier_info_domain = [
        ('partner_id', '=', vendor_id),
        ('product_id', '=', product['id'])
    ]
    supplier_info = odoo.search_read('product.supplierinfo', supplier_info_domain,
                                      ['price', 'min_qty'], limit=1)

    if supplier_info:
        product['supplier_price'] = supplier_info[0]['price']
        product['min_qty'] = supplier_info[0].get('min_qty', 0)
    else:
        product['supplier_price'] = product.get('standard_price', 0)
        product['min_qty'] = 0

    return product


def create_purchase_order(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a purchase order in Odoo.

    Args:
        odoo: Odoo connection
        params: Validated input parameters

    Returns:
        Result dict with order details
    """
    # Lookup vendor
    vendor = lookup_vendor(odoo, params)
    vendor_id = vendor['id']

    # Prepare order header
    order_vals = {
        'partner_id': vendor_id,
    }

    # Optional fields
    if params.get('vendor_ref'):
        order_vals['partner_ref'] = params['vendor_ref']
    if params.get('expected_date'):
        order_vals['date_planned'] = params['expected_date']
    if params.get('notes'):
        order_vals['notes'] = params['notes']

    # Create the order
    order_id = odoo.create('purchase.order', order_vals)

    # Get the order reference
    order_data = odoo.read('purchase.order', [order_id], ['name', 'currency_id'])[0]
    order_ref = order_data['name']
    currency = order_data['currency_id'][1] if order_data.get('currency_id') else 'ZAR'

    # Create order lines
    order_lines = []
    total_amount = 0

    for product_info in params['products']:
        product = lookup_product(odoo, product_info, vendor_id)

        # Get price - use provided, supplier price, or standard price
        unit_price = product_info.get('unit_price') or product.get('supplier_price', 0)
        quantity = product_info['quantity']

        # Create line
        line_vals = {
            'order_id': order_id,
            'product_id': product['id'],
            'product_qty': quantity,
            'price_unit': unit_price,
        }

        # Set UoM if available
        if product.get('uom_po_id'):
            line_vals['product_uom'] = product['uom_po_id'][0]

        line_id = odoo.create('purchase.order.line', line_vals)

        subtotal = quantity * unit_price
        total_amount += subtotal

        order_lines.append({
            'line_id': line_id,
            'product': product['name'],
            'product_id': product['id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'uom': product['uom_po_id'][1] if product.get('uom_po_id') else 'Units',
            'subtotal': round(subtotal, 2)
        })

    # Optionally confirm the order
    if params.get('auto_confirm', False):
        odoo.execute('purchase.order', 'button_confirm', [order_id])
        order_data = odoo.read('purchase.order', [order_id], ['state'])[0]
        state = order_data['state']
    else:
        state = 'draft'

    return {
        'po_id': order_id,
        'po_ref': order_ref,
        'vendor': vendor['name'],
        'vendor_id': vendor_id,
        'order_lines': order_lines,
        'total_amount': round(total_amount, 2),
        'currency': currency,
        'expected_date': params.get('expected_date'),
        'state': state,
    }


def main(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function.

    Args:
        input_params: Dictionary with required parameters

    Returns:
        Dictionary with operation result (success/failure, data, messages)
    """
    with OperationLogger('process_purchase_order', input_params):
        try:
            # 1. Validate inputs
            validate_inputs(input_params)

            # 2. Connect to Odoo
            odoo = OdooConnection()

            # 3. Execute operation
            result = create_purchase_order(odoo, input_params)

            return {
                'status': 'success',
                'data': result,
                'message': f"Purchase Order {result['po_ref']} created for {result['vendor']}"
            }

        except ValueError as e:
            error_response = handle_error(e, {'operation': 'process_purchase_order', 'params': input_params})
            return error_response

        except OdooConnectionError as e:
            error_response = handle_error(e, {'operation': 'process_purchase_order'})
            return error_response

        except Exception as e:
            error_response = handle_error(e, {'operation': 'process_purchase_order', 'params': input_params})
            return error_response


if __name__ == '__main__':
    # CLI interface
    import argparse

    parser = argparse.ArgumentParser(description='Create Purchase Order in Odoo')
    parser.add_argument('--vendor', type=str, help='Vendor name')
    parser.add_argument('--vendor-id', type=int, help='Vendor ID')
    parser.add_argument('--product', type=str, help='Product name')
    parser.add_argument('--product-id', type=int, help='Product ID')
    parser.add_argument('--quantity', type=float, default=1, help='Quantity')
    parser.add_argument('--price', type=float, help='Unit price (optional)')
    parser.add_argument('--date', type=str, help='Expected delivery date')
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
            'vendor_name': args.vendor,
            'vendor_id': args.vendor_id,
            'products': [{
                'product_name': args.product,
                'product_id': args.product_id,
                'quantity': args.quantity,
                'unit_price': args.price,
            }],
            'expected_date': args.date,
            'auto_confirm': args.confirm,
        }

    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
