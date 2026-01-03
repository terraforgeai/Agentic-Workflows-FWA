#!/usr/bin/env python3
"""
Create Sales Order - Deterministic Odoo Operation

Purpose: Create a new Sales Order in Odoo with order lines
Input: Customer info, product lines with quantities and prices
Output: Created order ID, reference, and confirmation

Related Directive: directives/create_sales_order_directive.md
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
from field_mappings import SALE_ORDER_FIELDS, SALE_ORDER_LINE_FIELDS

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
    # Must have customer identifier
    if not params.get('customer_name') and not params.get('customer_id'):
        raise ValueError("Either 'customer_name' or 'customer_id' is required")

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


def lookup_customer(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find customer in Odoo.

    Args:
        odoo: Odoo connection
        params: Input parameters with customer_name or customer_id

    Returns:
        Customer data dict

    Raises:
        ValueError: If customer not found
    """
    if params.get('customer_id'):
        # Direct lookup by ID
        customers = odoo.read('res.partner', [params['customer_id']],
                              ['name', 'email', 'customer_rank'])
        if not customers:
            raise ValueError(f"Customer with ID {params['customer_id']} not found")
        return customers[0]

    # Search by name
    name = params['customer_name']
    domain = [('name', 'ilike', name), ('customer_rank', '>', 0)]
    customers = odoo.search_read('res.partner', domain,
                                  ['name', 'email', 'customer_rank'], limit=5)

    if not customers:
        # Try broader search
        domain = [('name', 'ilike', f'%{name}%')]
        all_partners = odoo.search_read('res.partner', domain, ['name'], limit=5)
        suggestions = [p['name'] for p in all_partners] if all_partners else []
        raise ValueError(f"Customer '{name}' not found. Similar: {suggestions}")

    if len(customers) > 1:
        # Multiple matches - return first but warn
        logger.warning(f"Multiple customers match '{name}'. Using: {customers[0]['name']}")

    return customers[0]


def lookup_product(odoo: OdooConnection, product_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find product in Odoo.

    Args:
        odoo: Odoo connection
        product_info: Product dict with product_name or product_id

    Returns:
        Product data dict

    Raises:
        ValueError: If product not found
    """
    if product_info.get('product_id'):
        products = odoo.read('product.product', [product_info['product_id']],
                             ['name', 'list_price', 'uom_id', 'sale_ok'])
        if not products:
            raise ValueError(f"Product with ID {product_info['product_id']} not found")
        if not products[0].get('sale_ok'):
            raise ValueError(f"Product '{products[0]['name']}' is not available for sale")
        return products[0]

    # Search by name
    name = product_info['product_name']
    domain = [('name', 'ilike', name), ('sale_ok', '=', True)]
    products = odoo.search_read('product.product', domain,
                                 ['name', 'list_price', 'uom_id'], limit=5)

    if not products:
        raise ValueError(f"Product '{name}' not found or not available for sale")

    if len(products) > 1:
        # Look for exact match
        exact = [p for p in products if p['name'].lower() == name.lower()]
        if exact:
            return exact[0]
        logger.warning(f"Multiple products match '{name}'. Using: {products[0]['name']}")

    return products[0]


def create_sales_order(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a sales order in Odoo.

    Args:
        odoo: Odoo connection
        params: Validated input parameters

    Returns:
        Result dict with order details
    """
    # Lookup customer
    customer = lookup_customer(odoo, params)
    customer_id = customer['id']

    # Prepare order header
    order_vals = {
        'partner_id': customer_id,
    }

    # Optional fields
    if params.get('customer_ref'):
        order_vals['client_order_ref'] = params['customer_ref']
    if params.get('notes'):
        order_vals['note'] = params['notes']
    if params.get('delivery_date'):
        order_vals['commitment_date'] = params['delivery_date']

    # Create the order
    order_id = odoo.create('sale.order', order_vals)

    # Get the order reference
    order_data = odoo.read('sale.order', [order_id], ['name'])[0]
    order_ref = order_data['name']

    # Create order lines
    order_lines = []
    total_amount = 0

    for product_info in params['products']:
        product = lookup_product(odoo, product_info)

        # Get price - use provided or default
        unit_price = product_info.get('unit_price', product['list_price'])
        quantity = product_info['quantity']
        discount = product_info.get('discount', 0)

        # Create line
        line_vals = {
            'order_id': order_id,
            'product_id': product['id'],
            'product_uom_qty': quantity,
            'price_unit': unit_price,
            'discount': discount,
        }

        line_id = odoo.create('sale.order.line', line_vals)

        # Calculate subtotal
        subtotal = quantity * unit_price * (1 - discount / 100)
        total_amount += subtotal

        order_lines.append({
            'line_id': line_id,
            'product': product['name'],
            'product_id': product['id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'discount': discount,
            'subtotal': round(subtotal, 2)
        })

    # Optionally confirm the order
    if params.get('auto_confirm', False):
        odoo.execute('sale.order', 'action_confirm', [order_id])
        order_data = odoo.read('sale.order', [order_id], ['state'])[0]
        state = order_data['state']
    else:
        state = 'draft'

    return {
        'order_id': order_id,
        'order_ref': order_ref,
        'customer': customer['name'],
        'customer_id': customer_id,
        'order_lines': order_lines,
        'total_amount': round(total_amount, 2),
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
    with OperationLogger('create_sales_order', input_params):
        try:
            # 1. Validate inputs
            validate_inputs(input_params)

            # 2. Connect to Odoo
            odoo = OdooConnection()

            # 3. Execute operation
            result = create_sales_order(odoo, input_params)

            return {
                'status': 'success',
                'data': result,
                'message': f"Sales Order {result['order_ref']} created successfully for {result['customer']}"
            }

        except ValueError as e:
            error_response = handle_error(e, {'operation': 'create_sales_order', 'params': input_params})
            return error_response

        except OdooConnectionError as e:
            error_response = handle_error(e, {'operation': 'create_sales_order'})
            return error_response

        except Exception as e:
            error_response = handle_error(e, {'operation': 'create_sales_order', 'params': input_params})
            return error_response


if __name__ == '__main__':
    # CLI interface
    import argparse

    parser = argparse.ArgumentParser(description='Create Sales Order in Odoo')
    parser.add_argument('--customer', type=str, help='Customer name')
    parser.add_argument('--customer-id', type=int, help='Customer ID')
    parser.add_argument('--product', type=str, help='Product name')
    parser.add_argument('--product-id', type=int, help='Product ID')
    parser.add_argument('--quantity', type=float, default=1, help='Quantity')
    parser.add_argument('--price', type=float, help='Unit price (optional)')
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
            'customer_name': args.customer,
            'customer_id': args.customer_id,
            'products': [{
                'product_name': args.product,
                'product_id': args.product_id,
                'quantity': args.quantity,
                'unit_price': args.price,
            }],
            'auto_confirm': args.confirm,
        }

    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
