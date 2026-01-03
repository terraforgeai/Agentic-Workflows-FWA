# Manage Inventory Directive

## Purpose
Manage inventory operations in Odoo including stock checks, transfers between locations, adjustments, and reporting for FWA's warehouse operations.

## Operations Covered
1. **Stock Check** - Query current stock levels
2. **Stock Transfer** - Move items between locations
3. **Stock Adjustment** - Correct inventory discrepancies
4. **Stock Report** - Generate inventory reports

---

## Operation 1: Stock Check

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| product_name | string | No | "Golf Shirt - Blue" |
| product_id | integer | No | 123 |
| location | string | No | "WHFWA/Stock" |
| include_reserved | boolean | No | true (default: false) |

### Steps
1. Search stock.quant for matching criteria
2. Aggregate quantities by product/location
3. Calculate available vs reserved

### Output
```json
{
  "status": "success",
  "stock_levels": [
    {
      "product": "Golf Shirt - Blue - Size M",
      "location": "WHFWA/Stock",
      "on_hand": 250,
      "reserved": 50,
      "available": 200
    }
  ]
}
```

---

## Operation 2: Stock Transfer

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| product_id | integer | Yes | 123 |
| quantity | float | Yes | 100 |
| from_location | string | Yes | "WHFWA/Stock" |
| to_location | string | Yes | "WHFWA/Pre-Production" |
| reference | string | No | "Internal Transfer" |

### Steps
1. Validate locations exist
2. Check sufficient stock at source
3. Create stock.picking (internal transfer)
4. Validate transfer (move stock)

### Output
```json
{
  "status": "success",
  "picking_id": 456,
  "picking_ref": "WH/INT/00123",
  "product": "Golf Shirt - Blue - Size M",
  "quantity": 100,
  "from": "WHFWA/Stock",
  "to": "WHFWA/Pre-Production",
  "state": "done"
}
```

---

## Operation 3: Stock Adjustment

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| product_id | integer | Yes | 123 |
| location | string | Yes | "WHFWA/Stock" |
| new_quantity | float | Yes | 245 |
| reason | string | Yes | "Physical count correction" |

### Steps
1. Get current stock level
2. Create inventory adjustment
3. Apply adjustment
4. Log change with reason

### Output
```json
{
  "status": "success",
  "adjustment_id": 789,
  "product": "Golf Shirt - Blue - Size M",
  "location": "WHFWA/Stock",
  "old_quantity": 250,
  "new_quantity": 245,
  "difference": -5,
  "reason": "Physical count correction"
}
```

---

## Operation 4: Stock Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| report_type | string | Yes | "low_stock" / "all" / "location" |
| threshold | float | No | 50 (for low_stock) |
| location | string | No | "WHFWA/Stock" |
| category | string | No | "Finished Goods" |

### Steps
1. Query stock.quant with filters
2. Aggregate and format data
3. Calculate reorder suggestions

### Output
```json
{
  "status": "success",
  "report_type": "low_stock",
  "threshold": 50,
  "items": [
    {
      "product": "Golf Shirt - Blue - Size M",
      "location": "WHFWA/Stock",
      "on_hand": 25,
      "reorder_point": 100,
      "suggested_order": 75
    }
  ],
  "total_items": 1
}
```

---

## Prerequisites
- [ ] Odoo connection active
- [ ] Inventory module configured
- [ ] Warehouse locations created
- [ ] User has Inventory / User permissions

## FWA Warehouse Locations

| Location Code | Purpose |
|---------------|---------|
| `WHFWA/Stock` | Main finished goods storage |
| `WHFWA/Pre-Production` | Components staged for manufacturing |
| `WHFWA/Subcontracting` | Items at subcontractor |
| `WHFWA/Quality Control` | Items awaiting QC |
| `WHFWA/Input` | Receiving area |
| `WHFWA/Output` | Shipping area |

## Edge Cases

### Insufficient stock for transfer
- Return error with current levels
- Suggest alternative: partial transfer or wait

### Location not found
- Search with fuzzy matching
- Return list of valid locations

### Negative stock after adjustment
- Warning returned (may be valid for backorders)
- Require confirmation for negative adjustments

### Reserved stock conflicts
- Cannot transfer reserved stock
- Return reservation details

## Related Scripts
- `execution/manage_inventory.py`
- `execution/bulk_inventory_import.py`

## Odoo Models Used
- `stock.quant` - Current stock levels
- `stock.picking` - Transfers/moves
- `stock.location` - Warehouse locations
- `stock.move` - Individual item moves
- `stock.inventory` - Adjustments (older method)
- `stock.quant` - Direct quantity adjustments (newer)

## API Notes
- Use `stock.quant` for reading current stock
- Use `stock.picking` for transfers
- Adjustments can be done via quant updates or inventory adjustments
- Always include lot/serial if product requires tracking

## Last Updated
2 January 2026 - Initial directive creation
