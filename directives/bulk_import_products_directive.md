# Bulk Import Products Directive

## Purpose
Import multiple products into Odoo from CSV/Excel files or structured data. Used for initial product catalog setup or adding new product lines.

## Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| source_type | string | Yes | "csv", "excel", "json" |
| file_path | string | Yes* | ".tmp/odoo_exports/products.csv" |
| data | list | Yes* | Direct JSON data (*either file or data) |
| update_existing | boolean | No | false (default: create only) |
| dry_run | boolean | No | true (validate without creating) |

### Product Data Structure
```json
{
  "name": "Golf Shirt - Blue - Size M",
  "default_code": "GS-BLU-M",
  "barcode": "6001234567890",
  "type": "product",
  "category": "FWA / Finished Goods",
  "list_price": 450.00,
  "standard_price": 180.00,
  "uom": "Units",
  "tracking": "none",
  "sale_ok": true,
  "purchase_ok": true,
  "description": "Premium golf shirt, blue, medium size"
}
```

### CSV Format
```csv
name,default_code,barcode,type,category,list_price,standard_price
Golf Shirt - Blue - Size S,GS-BLU-S,6001234567891,product,FWA / Finished Goods,450.00,180.00
Golf Shirt - Blue - Size M,GS-BLU-M,6001234567892,product,FWA / Finished Goods,450.00,180.00
Golf Shirt - Blue - Size L,GS-BLU-L,6001234567893,product,FWA / Finished Goods,450.00,180.00
```

## Prerequisites
- [ ] Odoo connection active
- [ ] Product categories exist in Odoo
- [ ] Units of Measure configured
- [ ] User has Sales / Manager or Inventory / Manager permissions
- [ ] Source file accessible and properly formatted

## Steps
1. **Validate source**
   - Check file exists and is readable
   - Parse CSV/Excel/JSON
   - Validate required columns present

2. **Validate each product**
   - Required fields: name
   - Check category exists
   - Check UoM exists
   - Validate field types (prices are numbers, etc.)

3. **Check for duplicates**
   - Search by default_code (SKU)
   - Search by barcode
   - Flag duplicates based on update_existing setting

4. **Dry run (if requested)**
   - Report what would be created/updated
   - List any validation errors
   - Return without making changes

5. **Create/Update products**
   - For each valid product:
     - Lookup category ID
     - Lookup UoM ID
     - Create product.product record
   - Track successes and failures

6. **Return results**
   - Count of created/updated/failed
   - List of errors with row numbers
   - IDs of created products

## Outputs

### Success
```json
{
  "status": "success",
  "summary": {
    "total_rows": 50,
    "created": 48,
    "updated": 0,
    "skipped": 2,
    "failed": 0
  },
  "created_products": [
    {"id": 101, "name": "Golf Shirt - Blue - Size S", "sku": "GS-BLU-S"},
    {"id": 102, "name": "Golf Shirt - Blue - Size M", "sku": "GS-BLU-M"}
  ],
  "skipped": [
    {"row": 15, "reason": "Duplicate SKU: GS-BLU-M already exists"}
  ],
  "message": "Imported 48 products successfully"
}
```

### Dry Run Result
```json
{
  "status": "success",
  "dry_run": true,
  "summary": {
    "total_rows": 50,
    "would_create": 48,
    "would_update": 0,
    "would_skip": 2,
    "errors": 0
  },
  "validation_errors": [],
  "message": "Dry run complete. 48 products ready to import."
}
```

### Failure
```json
{
  "status": "error",
  "error_type": "validation",
  "summary": {
    "total_rows": 50,
    "valid": 45,
    "invalid": 5
  },
  "validation_errors": [
    {"row": 12, "field": "list_price", "error": "Invalid number: 'abc'"},
    {"row": 23, "field": "category", "error": "Category 'Unknown' not found"}
  ],
  "message": "5 validation errors found. Fix errors and retry."
}
```

## Edge Cases

### Duplicate SKU/Barcode
- If update_existing = false: Skip and report
- If update_existing = true: Update existing record

### Category not found
- Return error with row number
- Suggest similar category names

### Invalid data types
- Prices must be numbers
- Boolean fields accept: true/false, 1/0, yes/no

### Large file (1000+ products)
- Process in batches of 100
- Report progress
- Allow resume on failure

### Missing optional fields
- Use defaults from field_mappings.py
- type defaults to 'product'
- sale_ok/purchase_ok default to true

## Field Mappings

| CSV Column | Odoo Field | Type | Default |
|------------|------------|------|---------|
| name | name | char | (required) |
| default_code | default_code | char | |
| sku | default_code | char | (alias) |
| barcode | barcode | char | |
| type | type | selection | product |
| category | categ_id | many2one | |
| list_price | list_price | float | 0.0 |
| sale_price | list_price | float | (alias) |
| standard_price | standard_price | float | 0.0 |
| cost | standard_price | float | (alias) |
| uom | uom_id | many2one | Units |
| tracking | tracking | selection | none |
| sale_ok | sale_ok | boolean | true |
| purchase_ok | purchase_ok | boolean | true |
| active | active | boolean | true |
| description | description | text | |
| description_sale | description_sale | text | |

## Related Scripts
- `execution/bulk_import_products.py`

## FWA Product Categories
- `FWA / Finished Goods` - Golf shirts, caps, branded items
- `FWA / Raw Materials` - Fabrics, thread, labels
- `FWA / Components` - Buttons, zippers
- `FWA / Packaging` - Bags, boxes

## API Notes
- Use product.template for base products
- Variants auto-created if attributes defined
- Large imports: consider using Odoo's import queue

## Last Updated
2 January 2026 - Initial directive creation
