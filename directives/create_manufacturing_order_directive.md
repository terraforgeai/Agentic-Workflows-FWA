# Create Manufacturing Order Directive

## Purpose
Create a Manufacturing Order (MO) in Odoo to produce finished goods (golf shirts, branded apparel) from raw materials and components. This is used for CMT (Cut, Make, Trim) subcontracting operations.

## Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| product_name | string | Yes* | "Golf Shirt - Blue - Size M" |
| product_id | integer | Yes* | 123 (*either name or ID required) |
| quantity | float | Yes | 500 |
| bom_id | integer | No | 45 (uses default BOM if not specified) |
| scheduled_date | datetime | No | "2026-01-10 08:00:00" |
| origin | string | No | "S00123" (source sales order) |
| notes | string | No | "Rush order - priority" |

## Prerequisites
- [ ] Odoo connection active
- [ ] Product exists with type = 'product' (storable)
- [ ] Bill of Materials (BOM) exists for the product
- [ ] Manufacturing module installed and configured
- [ ] User has Manufacturing / User permissions

## Steps
1. **Validate inputs**
   - Product name or ID provided
   - Quantity is positive
   - Check BOM exists

2. **Lookup product**
   - Search product.product by name or ID
   - Verify product type is 'product'
   - Get default UoM

3. **Lookup BOM**
   - If bom_id provided, verify it exists
   - Otherwise, find default BOM for product
   - Verify BOM is active

4. **Check component availability**
   - Get BOM components
   - Check stock levels for each
   - Calculate fabric consumption (1.5m per garment standard)

5. **Create Manufacturing Order**
   - Create mrp.production record
   - Set product, quantity, BOM
   - Set locations (Pre-Production → Stock)
   - Created in 'draft' state

6. **Optional: Confirm MO**
   - Call action_confirm() to reserve components
   - Creates work orders if routing defined

7. **Return result**
   - MO ID and reference
   - Component list with availability
   - Any shortages flagged

## Outputs

### Success
```json
{
  "status": "success",
  "mo_id": 789,
  "mo_ref": "MO/00045",
  "product": "Golf Shirt - Blue - Size M",
  "quantity": 500,
  "bom": "BOM/Golf Shirt - Blue",
  "components": [
    {"product": "Fabric - Blue Cotton", "qty_required": 750, "qty_available": 1000, "status": "available"},
    {"product": "Thread - Blue", "qty_required": 50, "qty_available": 200, "status": "available"},
    {"product": "Label - FWA", "qty_required": 500, "qty_available": 450, "status": "shortage"}
  ],
  "state": "draft",
  "message": "Manufacturing Order MO/00045 created. Note: Label shortage of 50 units."
}
```

### Failure
```json
{
  "status": "error",
  "error_type": "not_found",
  "message": "No BOM found for product 'Golf Shirt - Blue - Size M'",
  "suggestions": ["Create a BOM in Odoo Manufacturing", "Check product has correct BOM reference"]
}
```

## Edge Cases

### No BOM found
- Return error with suggestion to create BOM
- List similar products that have BOMs

### Component shortage
- MO still created (draft state)
- Return detailed shortage report
- Suggest creating purchase orders for missing items

### Product not storable
- Cannot manufacture services or consumables
- Return error with product type info

### Multiple BOMs exist
- Use BOM with sequence = 1 (default)
- Or return list for user to choose

### Subcontracting scenario
- If BOM has subcontractor, create subcontracting PO
- Components sent to subcontractor location

## Odoo Modules Involved
- **Manufacturing** (mrp) - Core MO management
- **Inventory** (stock) - Component checking, locations
- **Purchase** (purchase) - Subcontracting orders

## FWA-Specific Notes

### Fabric Consumption
- Standard: 1.5 meters per golf shirt
- T-shirts: 1.2 meters
- Calculate total fabric needed: quantity × consumption rate

### Warehouse Locations
- Components from: `WHFWA/Pre-Production`
- Finished goods to: `WHFWA/Stock`
- Subcontracting: `WHFWA/Subcontracting`

### Work Centers
- Cutting
- Sewing
- Quality Control
- Finishing

## Related Scripts
- `execution/create_manufacturing_order.py`

## API Notes
- MO created in 'draft' state by default
- action_confirm() reserves components
- action_assign() checks availability
- button_mark_done() completes the MO

## Last Updated
2 January 2026 - Initial directive creation
