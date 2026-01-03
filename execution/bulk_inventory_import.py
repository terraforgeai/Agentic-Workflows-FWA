#!/usr/bin/env python3
"""
Bulk Inventory Import - Deterministic Odoo Operation

Purpose: Import/update inventory levels from CSV or structured data
Input: Product-location-quantity data
Output: Updated stock levels, adjustment report

Related Directive: directives/manage_inventory_directive.md
"""

import os
import sys
import json
import csv
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from odoo_connect import OdooConnection, OdooConnectionError
from error_handler import handle_error, log_operation, OperationLogger
from field_mappings import STOCK_QUANT_FIELDS, FWA_LOCATIONS

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
    # Must have data source
    if not params.get('file_path') and not params.get('data'):
        raise ValueError("Either 'file_path' or 'data' is required")

    # If file, check it exists
    if params.get('file_path'):
        if not os.path.isfile(params['file_path']):
            raise ValueError(f"File not found: {params['file_path']}")


def parse_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse inventory data from CSV file.

    Expected columns: product_code, product_name, location, quantity

    Args:
        file_path: Path to CSV file

    Returns:
        List of inventory records
    """
    records = []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
            # Normalize column names
            normalized = {}
            for key, value in row.items():
                key_lower = key.lower().strip().replace(' ', '_')
                normalized[key_lower] = value.strip() if value else None

            # Map common variations
            record = {
                'row': row_num,
                'product_code': normalized.get('product_code') or normalized.get('sku') or normalized.get('default_code'),
                'product_name': normalized.get('product_name') or normalized.get('name') or normalized.get('product'),
                'location': normalized.get('location') or normalized.get('location_name') or 'WHFWA/Stock',
                'quantity': normalized.get('quantity') or normalized.get('qty') or normalized.get('on_hand'),
            }

            # Validate required fields
            if not record['product_code'] and not record['product_name']:
                logger.warning(f"Row {row_num}: No product identifier, skipping")
                continue

            # Parse quantity
            try:
                record['quantity'] = float(record['quantity']) if record['quantity'] else 0
            except ValueError:
                logger.warning(f"Row {row_num}: Invalid quantity '{record['quantity']}', defaulting to 0")
                record['quantity'] = 0

            records.append(record)

    return records


def lookup_product(odoo: OdooConnection, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Find product in Odoo.

    Args:
        odoo: Odoo connection
        record: Inventory record with product_code or product_name

    Returns:
        Product dict or None if not found
    """
    # Try by code first
    if record.get('product_code'):
        domain = [('default_code', '=', record['product_code'])]
        products = odoo.search_read('product.product', domain, ['name', 'type'], limit=1)
        if products:
            return products[0]

    # Try by name
    if record.get('product_name'):
        domain = [('name', 'ilike', record['product_name'])]
        products = odoo.search_read('product.product', domain, ['name', 'type'], limit=1)
        if products:
            return products[0]

    return None


def lookup_location(odoo: OdooConnection, location_name: str) -> Optional[Dict[str, Any]]:
    """
    Find location in Odoo.

    Args:
        odoo: Odoo connection
        location_name: Location name or path

    Returns:
        Location dict or None
    """
    # Try exact match first
    domain = [('complete_name', '=', location_name)]
    locations = odoo.search_read('stock.location', domain, ['name', 'complete_name'], limit=1)

    if locations:
        return locations[0]

    # Try partial match
    domain = [('complete_name', 'ilike', location_name), ('usage', '=', 'internal')]
    locations = odoo.search_read('stock.location', domain, ['name', 'complete_name'], limit=1)

    return locations[0] if locations else None


def update_inventory(odoo: OdooConnection, product_id: int, location_id: int,
                     new_quantity: float, reason: str = "Bulk import") -> Dict[str, Any]:
    """
    Update inventory quantity for a product at a location.

    Args:
        odoo: Odoo connection
        product_id: Product ID
        location_id: Location ID
        new_quantity: New quantity to set
        reason: Reason for adjustment

    Returns:
        Result dict with old/new quantities
    """
    # Get current quantity
    domain = [('product_id', '=', product_id), ('location_id', '=', location_id)]
    quants = odoo.search_read('stock.quant', domain, ['quantity'])

    current_qty = sum(q['quantity'] for q in quants) if quants else 0
    difference = new_quantity - current_qty

    if abs(difference) < 0.001:
        return {
            'adjusted': False,
            'old_quantity': current_qty,
            'new_quantity': new_quantity,
            'difference': 0,
            'message': 'No change needed'
        }

    # Update the quant directly (Odoo 14+ method)
    if quants:
        # Update existing quant
        quant_id = quants[0]['id']
        odoo.write('stock.quant', [quant_id], {'quantity': new_quantity})
    else:
        # Create new quant
        quant_vals = {
            'product_id': product_id,
            'location_id': location_id,
            'quantity': new_quantity,
        }
        odoo.create('stock.quant', quant_vals)

    return {
        'adjusted': True,
        'old_quantity': round(current_qty, 2),
        'new_quantity': round(new_quantity, 2),
        'difference': round(difference, 2),
        'message': f"Adjusted by {difference:+.2f}"
    }


def process_inventory_import(odoo: OdooConnection, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process inventory import.

    Args:
        odoo: Odoo connection
        params: Input parameters

    Returns:
        Result dict with import summary
    """
    # Get records from file or direct data
    if params.get('file_path'):
        records = parse_csv_file(params['file_path'])
    else:
        records = params['data']

    dry_run = params.get('dry_run', False)

    # Process results
    results = {
        'total_rows': len(records),
        'processed': 0,
        'adjusted': 0,
        'unchanged': 0,
        'skipped': 0,
        'errors': [],
        'adjustments': [],
    }

    for record in records:
        row_num = record.get('row', results['processed'] + 1)

        # Lookup product
        product = lookup_product(odoo, record)
        if not product:
            results['skipped'] += 1
            results['errors'].append({
                'row': row_num,
                'error': f"Product not found: {record.get('product_code') or record.get('product_name')}"
            })
            continue

        # Lookup location
        location = lookup_location(odoo, record['location'])
        if not location:
            results['skipped'] += 1
            results['errors'].append({
                'row': row_num,
                'error': f"Location not found: {record['location']}"
            })
            continue

        # Dry run - just report what would happen
        if dry_run:
            domain = [('product_id', '=', product['id']), ('location_id', '=', location['id'])]
            quants = odoo.search_read('stock.quant', domain, ['quantity'])
            current_qty = sum(q['quantity'] for q in quants) if quants else 0

            results['adjustments'].append({
                'row': row_num,
                'product': product['name'],
                'location': location['complete_name'],
                'current_qty': round(current_qty, 2),
                'new_qty': record['quantity'],
                'difference': round(record['quantity'] - current_qty, 2),
                'would_adjust': abs(record['quantity'] - current_qty) > 0.001
            })
            results['processed'] += 1
            continue

        # Actually update
        try:
            adjustment = update_inventory(
                odoo, product['id'], location['id'],
                record['quantity'], "Bulk import"
            )

            if adjustment['adjusted']:
                results['adjusted'] += 1
            else:
                results['unchanged'] += 1

            results['adjustments'].append({
                'row': row_num,
                'product': product['name'],
                'location': location['complete_name'],
                **adjustment
            })
            results['processed'] += 1

        except Exception as e:
            results['skipped'] += 1
            results['errors'].append({
                'row': row_num,
                'error': str(e)
            })

    return results


def main(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function.

    Args:
        input_params: Dictionary with required parameters

    Returns:
        Dictionary with operation result (success/failure, data, messages)
    """
    with OperationLogger('bulk_inventory_import', input_params):
        try:
            # 1. Validate inputs
            validate_inputs(input_params)

            # 2. Connect to Odoo
            odoo = OdooConnection()

            # 3. Execute operation
            result = process_inventory_import(odoo, input_params)

            dry_run_msg = " (DRY RUN)" if input_params.get('dry_run') else ""
            message = (f"Inventory import{dry_run_msg}: "
                       f"{result['processed']} processed, "
                       f"{result['adjusted']} adjusted, "
                       f"{result['unchanged']} unchanged, "
                       f"{result['skipped']} skipped")

            return {
                'status': 'success' if result['skipped'] == 0 else 'partial',
                'data': result,
                'message': message
            }

        except ValueError as e:
            error_response = handle_error(e, {'operation': 'bulk_inventory_import'})
            return error_response

        except OdooConnectionError as e:
            error_response = handle_error(e, {'operation': 'bulk_inventory_import'})
            return error_response

        except Exception as e:
            error_response = handle_error(e, {'operation': 'bulk_inventory_import'})
            return error_response


if __name__ == '__main__':
    # CLI interface
    import argparse

    parser = argparse.ArgumentParser(description='Bulk Import Inventory to Odoo')
    parser.add_argument('--file', type=str, help='Path to CSV file')
    parser.add_argument('--dry-run', action='store_true', help='Validate without making changes')
    parser.add_argument('--json', type=str, help='JSON input file or string')

    args = parser.parse_args()

    if args.json:
        if os.path.isfile(args.json):
            with open(args.json) as f:
                test_input = json.load(f)
        else:
            test_input = json.loads(args.json)
    else:
        test_input = {
            'file_path': args.file,
            'dry_run': args.dry_run,
        }

    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
