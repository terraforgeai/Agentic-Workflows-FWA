# Generate Reports Directive

## Purpose
Generate various reports from Odoo data for business intelligence, operational planning, and management decision-making.

## Available Reports

### 1. Sales Report
### 2. Inventory Report
### 3. Manufacturing Report
### 4. Purchase Report
### 5. BOM Report (Bill of Materials)

---

## Report 1: Sales Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| date_from | date | No | "2026-01-01" |
| date_to | date | No | "2026-01-31" |
| customer_id | integer | No | 42 |
| product_id | integer | No | 123 |
| state | string | No | "sale" (confirmed orders) |
| group_by | string | No | "customer", "product", "date" |

### Output
```json
{
  "status": "success",
  "report": "sales",
  "period": "2026-01-01 to 2026-01-31",
  "summary": {
    "total_orders": 45,
    "total_revenue": 1250000.00,
    "average_order_value": 27777.78
  },
  "data": [
    {
      "order_ref": "S00123",
      "date": "2026-01-05",
      "customer": "ACME Corp",
      "products": ["Golf Shirt - Blue x 500"],
      "total": 22500.00,
      "state": "sale"
    }
  ]
}
```

---

## Report 2: Inventory Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| location | string | No | "WHFWA/Stock" |
| category | string | No | "FWA / Finished Goods" |
| low_stock_only | boolean | No | true |
| threshold | float | No | 50 |
| include_value | boolean | No | true |

### Output
```json
{
  "status": "success",
  "report": "inventory",
  "location": "WHFWA/Stock",
  "summary": {
    "total_products": 150,
    "total_value": 850000.00,
    "low_stock_items": 12
  },
  "data": [
    {
      "product": "Golf Shirt - Blue - Size M",
      "sku": "GS-BLU-M",
      "on_hand": 250,
      "reserved": 50,
      "available": 200,
      "reorder_point": 100,
      "unit_cost": 180.00,
      "total_value": 45000.00
    }
  ]
}
```

---

## Report 3: Manufacturing Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| date_from | date | No | "2026-01-01" |
| date_to | date | No | "2026-01-31" |
| product_id | integer | No | 123 |
| state | string | No | "progress" |
| include_components | boolean | No | true |

### Output
```json
{
  "status": "success",
  "report": "manufacturing",
  "period": "2026-01-01 to 2026-01-31",
  "summary": {
    "total_orders": 25,
    "in_progress": 8,
    "completed": 15,
    "cancelled": 2,
    "total_produced": 12500
  },
  "data": [
    {
      "mo_ref": "MO/00045",
      "product": "Golf Shirt - Blue - Size M",
      "quantity": 500,
      "state": "progress",
      "scheduled_start": "2026-01-10",
      "components_available": true
    }
  ]
}
```

---

## Report 4: Purchase Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| date_from | date | No | "2026-01-01" |
| date_to | date | No | "2026-01-31" |
| vendor_id | integer | No | 78 |
| state | string | No | "purchase" |
| pending_only | boolean | No | true |

### Output
```json
{
  "status": "success",
  "report": "purchase",
  "period": "2026-01-01 to 2026-01-31",
  "summary": {
    "total_orders": 30,
    "total_spent": 450000.00,
    "pending_receipts": 5
  },
  "data": [
    {
      "po_ref": "P00089",
      "date": "2026-01-02",
      "vendor": "Fabric Supplier Co",
      "products": ["Cotton Fabric - Blue x 1000m"],
      "total": 12500.00,
      "state": "purchase",
      "expected_date": "2026-01-20"
    }
  ]
}
```

---

## Report 5: BOM Report

### Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| product_id | integer | No | 123 |
| bom_id | integer | No | 45 |
| include_costs | boolean | No | true |
| explode_levels | integer | No | 2 (nested BOMs) |

### Output
```json
{
  "status": "success",
  "report": "bom",
  "product": "Golf Shirt - Blue - Size M",
  "bom_ref": "BOM/Golf Shirt - Blue",
  "summary": {
    "total_components": 5,
    "total_cost": 180.00,
    "fabric_consumption": "1.5m"
  },
  "components": [
    {
      "product": "Cotton Fabric - Blue",
      "quantity": 1.5,
      "uom": "m",
      "unit_cost": 85.00,
      "total_cost": 127.50
    },
    {
      "product": "Thread - Blue",
      "quantity": 1,
      "uom": "Units",
      "unit_cost": 15.00,
      "total_cost": 15.00
    },
    {
      "product": "Label - FWA",
      "quantity": 1,
      "uom": "Units",
      "unit_cost": 5.00,
      "total_cost": 5.00
    }
  ]
}
```

---

## Output Formats

Reports can be exported in multiple formats:

| Format | Extension | Use Case |
|--------|-----------|----------|
| JSON | .json | API consumption, further processing |
| CSV | .csv | Excel, spreadsheets |
| PDF | .pdf | Printing, sharing (future) |

Specify format with `output_format` parameter (default: json)

## Prerequisites
- [ ] Odoo connection active
- [ ] User has access to relevant modules
- [ ] Date ranges are valid

## Related Scripts
- `execution/generate_reports.py`

## FWA-Specific Reports

### Weekly Production Schedule
- Manufacturing orders for next 7 days
- Grouped by product
- Component availability check

### Monthly Sales Summary
- Sales by customer
- Top products
- Revenue trends

### Stock Reorder Report
- Items below reorder point
- Suggested purchase quantities
- Supplier information

## API Notes
- Large date ranges may timeout - use pagination
- Reports cached for 5 minutes (configurable)
- Export to `.tmp/odoo_exports/` directory

## Last Updated
2 January 2026 - Initial directive creation
