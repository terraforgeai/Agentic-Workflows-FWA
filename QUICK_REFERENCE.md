# FWA Odoo Quick Reference Card
## One-Page Guide for Daily Operations

---

## The 3-Layer System Explained

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: DIRECTIVES                                 │
│ (What to do - plain English instructions)          │
│ Location: directives/*.md                          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Layer 2: YOU (Claude in VS Code)                    │
│ (Decision making & orchestration)                  │
│ Read directive → Validate input → Call script      │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Layer 3: EXECUTION SCRIPTS                          │
│ (Deterministic Python → Odoo API)                  │
│ Location: execution/*.py                           │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start (5 Minutes)

### 1️⃣ Open FWA in VS Code
```bash
cd C:\Clients\FWA
code .
```

### 2️⃣ Tell Claude What You Need
```
"Create a sales order for 500 golf shirts for ACME Corp, due Feb 15"
```

### 3️⃣ Claude Does the Rest
- Reads directive
- Validates input
- Creates order
- Confirms with you

### 4️⃣ Check Results in Odoo
```
Sales > Orders > Find SO/2026/... > Confirm
```

---

## Core Workflows

### 📋 Create Sales Order
**Request:** "Create SO for 500 golf shirts (blue) for ABC Corp, delivery Feb 15"
**Input:** Customer, Product, Qty, Delivery Date
**Output:** Sales Order ID (e.g., SO/2026/001234)
**Next:** Confirm order in Odoo

### 🏭 Create Manufacturing Order  
**Request:** "Create MO to manufacture 500 golf shirts (blue), ready by Feb 1"
**Input:** Product, Quantity, Target Date
**Output:** Manufacturing Order ID (e.g., MO/2026/001)
**Next:** Manufacturing team picks components

### 🛒 Process Purchase Order
**Request:** "Create PO to order 1000m Piqué Knit from ABC Fabrics"
**Input:** Supplier, Product, Qty, Delivery Date
**Output:** Purchase Order ID (e.g., PO/2026/001)
**Next:** Approve and send to supplier

### 📦 Manage Inventory
**Request:** "Import stock levels from attached CSV file"
**Input:** CSV with products + quantities
**Output:** Stock updated in Odoo
**Next:** Verify in Inventory > Stock

---

## Common Commands

### Connection Test
```bash
python execution/odoo_connect.py --test
# Expected: ✅ Connected to Odoo [terraforegfwa]
```

### Check Logs
```bash
# View today's operations
cat .tmp/audit_logs/operations_20260102.log

# View errors
grep ERROR .tmp/audit_logs/*.log
```

### View Odoo Field Definitions
```bash
python execution/field_mappings.py
# Shows all available fields for each model
```

---

## Input Format Guide

| Field | Format | Example | Notes |
|-------|--------|---------|-------|
| **Customer** | integer ID | `5` | Must exist in Odoo |
| **Product** | integer ID | `10` | Must exist in Odoo |
| **Quantity** | positive number | `500` or `500.5` | Must be > 0 |
| **Date** | YYYY-MM-DD | `2026-02-15` | Future date only |
| **Price** | decimal | `8.50` | USD currency |
| **SKU** | alphanumeric | `GS-BLUE-M` | Unique identifier |

---

## Odoo Field Reference (Key Models)

### 📊 SALE.ORDER (Sales Order)
```
Required:
  - partner_id: Customer ID
  - order_line: Items in order
    - product_id: Product ID
    - product_qty: Quantity
    - price_unit: Unit price

Optional:
  - date_order: When ordered (default: today)
  - expected_date: Delivery date
  - warehouse_id: Which warehouse
  - note: Special instructions
```

### 🏭 MRP.PRODUCTION (Manufacturing Order)
```
Required:
  - product_id: What to make
  - product_qty: How many units
  - bom_id: Bill of Materials (recipe)
  - location_src_id: Where to get materials
  - location_dest_id: Where to put finished goods

Key:
  - state: draft → confirmed → progress → done
```

### 🛍️ PRODUCT.PRODUCT (Product)
```
Required:
  - name: Clear description
  - categ_id: Product category
  - type: 'product', 'service', or 'consu'

Key:
  - default_code: SKU/product code
  - list_price: Selling price
  - standard_price: Cost
  - uom_id: Unit of measure
```

### 🤝 RES.PARTNER (Customer/Supplier)
```
Required:
  - name: Company name
  - is_company: True for companies

Key:
  - email: Contact email
  - phone: Contact phone
  - customer_rank: 0=not customer, >0=customer
  - supplier_rank: 0=not supplier, >0=supplier
```

---

## Error Messages & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| **Customer not found** | ID doesn't exist | Verify ID in Sales > Customers |
| **Product not found** | ID doesn't exist | Verify ID in Sales > Products |
| **Insufficient stock** | Not enough units | MO created if MTO, else reduce qty |
| **Date in past** | Invalid delivery date | Use future date (YYYY-MM-DD) |
| **Authentication failed** | Bad credentials | Check .env file, test Odoo login |
| **Permission denied** | User can't access module | Check user group in Odoo settings |
| **Field required** | Missing required field | All fields marked "required" must be filled |

---

## Odoo Shortcuts

| Action | Path |
|--------|------|
| Create Sales Order | Sales > Orders > Create |
| View all Orders | Sales > Orders > List |
| Create Product | Sales > Products > Create |
| View Stock | Inventory > Products > Stock |
| Create PO | Purchase > Orders > Create |
| View Warehouse | Inventory > Warehouses > List |
| Check User Permissions | Settings > Users > [User] > Groups |

---

## FWA Data Structure Quick Reference

### 🏢 Company
- **Name:** Faith Wear Apparel
- **Address:** 47 Churchill Avenue, Alex Park, Harare, Zimbabwe
- **Timezone:** GMT+2 (Africa/Harare)
- **Currency:** USD

### 🏭 Warehouse
- **Code:** WHFWA
- **Name:** Faith Wear Apparel

### 📍 Stock Locations
- `WHFWA/Stock` - Main storage
- `WHFWA/Pre-Production` - Component staging
- `WHFWA/Subcontracting` - Subcontractor deliveries

### 📦 Product Categories
- Goods/Apparel/Golf Shirts
- Goods/Apparel/T-Shirts
- Goods/Apparel/Trousers
- Goods/Apparel/Aprons
- Goods/Apparel/Caps
- Goods/Fabrics/Knits
- Goods/Fabrics/Woven

### 🧵 Key Materials
- Piqué Knit (white, black, etc.)
- Woven Fabric (cotton, blends)
- Buttons (various sizes)
- Labels (brand labels)
- Thread (various colors)
- Zippers

### 👕 Key Products
- Golf Shirt - Various colors & sizes
- T-Shirt - Various colors & sizes
- Trousers - Various colors & sizes
- Caps - Various colors
- Aprons - With/without pockets

---

## Best Practices

✅ **DO:**
- [ ] Be specific: "500 golf shirts (blue, size M)" not "some shirts"
- [ ] Verify customer/product exists first
- [ ] Use small test quantities before bulk orders
- [ ] Check audit logs weekly
- [ ] Report errors with full context
- [ ] Keep .env secure (never share)

❌ **DON'T:**
- [ ] Assume products exist - verify first
- [ ] Order huge quantities for testing
- [ ] Modify .env file
- [ ] Share credentials
- [ ] Ignore error messages
- [ ] Bypass the 3-layer system

---

## File Locations

```
C:\Clients\FWA\                      ← Root directory
├── .env                             ← Your credentials (KEEP SECRET!)
├── FWA_CLAUDE.md                    ← System architecture (read first)
├── FWA_README.md                    ← Quick start guide
├── IMPLEMENTATION_CHECKLIST.md      ← Go-live checklist
│
├── directives\                      ← Workflow instructions
│   ├── create_sales_order_directive.md
│   ├── create_manufacturing_order_directive.md
│   └── ...
│
├── execution\                       ← Python scripts
│   ├── odoo_connect.py             ← Connection module
│   ├── error_handler.py            ← Error handling
│   ├── field_mappings.py           ← Data model reference
│   ├── create_sales_order.py       ← Create SO script
│   └── ...
│
└── .tmp\                            ← Temporary files (auto-generated)
    ├── audit_logs\                 ← Operation logs
    └── odoo_exports/            ← Exported data
```

---

## Getting Help

### Problem? Follow These Steps:

1. **Check the Error Message**
   - Copy the full error text
   - What does it say went wrong?

2. **Read the Directive**
   - `directives/[operation].md`
   - Check "Edge Cases" section
   - Look for similar scenario

3. **Review the Script**
   - `execution/[script].py`
   - Check validation logic
   - Look at error handling

4. **Check the Logs**
   - `.tmp/audit_logs/`
   - Find detailed error message
   - Note timestamps and context

5. **Ask for Help**
   - Tell Claude the problem
   - Share the full error message
   - Describe what you were trying to do

### Quick Help Links:
- 📚 Documentation: FWA_CLAUDE.md
- 🚀 Getting Started: FWA_README.md
- ✅ Setup Verification: IMPLEMENTATION_CHECKLIST.md
- 📖 Specific Workflow: directives/*.md
- 🔧 Field Reference: execution/field_mappings.py

---

## Support Contact

**Odoo Implementation Lead:** [Name]  
**Email:** [email]  
**Phone:** [phone]  
**Slack:** #fwa-odoo-automation  
**Hours:** [availability]

---

**Keep this card handy for daily operations!**  
*Last Updated: 2 January 2026*
