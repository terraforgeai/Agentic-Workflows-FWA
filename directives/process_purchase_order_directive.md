# Process Purchase Order Directive

## Purpose
Create and manage Purchase Orders in Odoo for ordering raw materials (fabrics, labels, packaging), finished goods from suppliers, or subcontracting services.

## Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| vendor_name | string | Yes* | "Fabric Supplier Co" |
| vendor_id | integer | Yes* | 78 (*either name or ID required) |
| products | list | Yes | See product structure below |
| expected_date | date | No | "2026-01-20" |
| vendor_ref | string | No | "INV-2026-001" |
| notes | string | No | "Quality inspection required" |

### Product Structure
```json
{
  "product_name": "Cotton Fabric - Blue",
  "product_id": 234,  // Optional if name provided
  "quantity": 1000,
  "unit_price": 12.50,  // Optional - uses supplier price if not provided
  "uom": "m"  // Optional - meters, units, etc.
}
```

## Prerequisites
- [ ] Odoo connection active
- [ ] Vendor exists in Odoo (res.partner with supplier_rank > 0)
- [ ] Products exist and are purchasable (purchase_ok = True)
- [ ] User has Purchase / User permissions

## Steps
1. **Validate inputs**
   - Vendor name or ID provided
   - At least one product line
   - Quantities are positive

2. **Lookup vendor**
   - Search res.partner by name or ID
   - Verify supplier_rank > 0
   - Get payment terms, currency

3. **Lookup products**
   - Search product.product by name or ID
   - Verify purchase_ok = True
   - Get supplier price from product.supplierinfo

4. **Create Purchase Order**
   - Create purchase.order header
   - Create purchase.order.line for each product
   - Order created in 'draft' state (RFQ)

5. **Optional: Confirm order**
   - Call button_confirm() to confirm PO
   - Creates incoming shipment (stock.picking)

6. **Return result**
   - PO ID and reference number
   - Order line details
   - Expected delivery info

## Outputs

### Success
```json
{
  "status": "success",
  "po_id": 567,
  "po_ref": "P00089",
  "vendor": "Fabric Supplier Co",
  "total_amount": 12500.00,
  "currency": "ZAR",
  "order_lines": [
    {"product": "Cotton Fabric - Blue", "qty": 1000, "uom": "m", "subtotal": 12500.00}
  ],
  "expected_date": "2026-01-20",
  "state": "draft",
  "message": "Purchase Order P00089 created successfully"
}
```

### Failure
```json
{
  "status": "error",
  "error_type": "not_found",
  "message": "Vendor 'Fabric Supplier' not found in Odoo",
  "suggestions": ["Check spelling", "Use vendor_id if known", "Create vendor first"]
}
```

## Edge Cases

### Vendor not found
- Search with fuzzy matching
- Return list of similar vendors
- Option to create new vendor

### Product not purchasable
- Return error with product info
- Check if product has purchase_ok = False

### No supplier price defined
- Use standard_price as fallback
- Warning returned about missing supplier price

### Subcontracting order
- If product has subcontractor BOM:
  - Create subcontracting PO
  - Components automatically reserved
  - Track component delivery to subcontractor

### Multiple currencies
- Use vendor's default currency
- Or specify currency in input

## Odoo Modules Involved
- **Purchase** (purchase) - Core PO management
- **Inventory** (stock) - Receipt creation
- **Subcontracting** (mrp_subcontracting) - If subcontracting

## FWA-Specific Notes

### Common Raw Materials
| Material | Unit | Typical Suppliers |
|----------|------|-------------------|
| Cotton Fabric | m | Fabric Mills |
| Polyester Fabric | m | Fabric Mills |
| Labels | units | Label Suppliers |
| Thread | units | Thread Suppliers |
| Packaging | units | Packaging Suppliers |

### Subcontracting Flow
1. Create subcontracting PO
2. Components automatically picked
3. Send components to subcontractor
4. Receive finished goods back

### Lead Times
- Fabric: 14-21 days
- Labels: 7-10 days
- Finished goods (subcontracted): 14-28 days

## Related Scripts
- `execution/process_purchase_order.py`

## API Notes
- PO created in 'draft' state (RFQ)
- button_confirm() confirms the order
- Incoming shipment auto-created on confirmation
- button_approve() if approval required

## Last Updated
2 January 2026 - Initial directive creation
