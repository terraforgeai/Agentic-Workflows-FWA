# Faith Wear Apparel - Claude Code Setup
## Quick Start Guide

Welcome! This guide helps you set up Claude Code in VS Code to automate FWA's Odoo operations.

---

## What This Does

This system lets you automate FWA's Odoo workflows from VS Code using Claude Code:

**Example commands:**
- "Create a sales order for 500 golf shirts for ACME Corp"
- "Import the attached inventory file into Odoo"
- "Generate a work order for manufacturing 200 blank t-shirts"
- "Check stock levels and alert me if anything is below 50 units"

Instead of manually clicking through Odoo, Claude orchestrates the operation and reports back.

---

## Prerequisites

### 1. Odoo Access
- ✅ Access to Odoo Online (terraforegfwa) as admin or privileged user
- ✅ Odoo API credentials (username, password or API key)
- ✅ Understanding of FWA's Odoo setup (sales, manufacturing, inventory)

### 2. Local Setup
- ✅ Python 3.8+ installed
- ✅ VS Code with Claude Code extension
- ✅ Git (optional, for version control)

### 3. Required Python Packages
```bash
pip install xmlrpc-client  # For Odoo RPC
pip install python-dotenv   # For .env file management
pip install requests         # For API calls
```

---

## Directory Structure

After setup, your FWA folder will look like this:

```
FWA/
├── .env                      # YOUR CREDENTIALS (keep secret!)
├── .gitignore               # Git ignore (protects .env)
├── FWA_CLAUDE.md            # Architecture & principles
├── FWA_README.md            # This file
│
├── directives/              # Workflow instruction files
│   ├── create_sales_order.md
│   ├── create_manufacturing_order.md
│   ├── process_purchase_order.md
│   ├── manage_inventory.md
│   └── ...
│
├── execution/               # Python scripts (Layer 3)
│   ├── odoo_connect.py
│   ├── create_sales_order.py
│   ├── field_mappings.py
│   ├── error_handler.py
│   └── ...
│
└── .tmp/                    # Temporary files (auto-generated)
    ├── audit_logs/
    └── odoo_exports/
```

---

## Setup Steps

### Step 1: Create the FWA Directory
```bash
# Already created at: C:\Clients\FWA
# All files should be copied to this location
cd C:\Clients\FWA
```

### Step 2: Create .env File
Create a file named `.env` in the FWA folder:

```
# Odoo Connection (KEEP THIS PRIVATE!)
ODOO_URL=https://terraforegfwa.odoo.com
ODOO_DB=terraforegfwa
ODOO_USERNAME=your_email@example.com
ODOO_PASSWORD=your_password_or_api_token

# Optional: Logging
LOG_LEVEL=INFO
LOG_PATH=.tmp/audit_logs/
```

**⚠️ Security Note:** 
- Never share your `.env` file
- Never commit it to GitHub
- Create a `.gitignore`:
  ```
  .env
  .tmp/
  __pycache__/
  *.pyc
  ```

### Step 3: Copy Core Files

Copy all provided files to `C:\Clients\FWA\`:
- FWA_CLAUDE.md (architecture guide)
- FWA_README.md (this file)
- All files from `directives\` folder
- All files from `execution\` folder

### Step 4: Test the Connection

From VS Code terminal in `C:\Clients\FWA`:
```bash
python execution/odoo_connect.py --test
```

Expected output:
```
✅ Connected to Odoo [terraforegfwa]
User: your_email@example.com
API: Ready
```

If it fails, check:
- [ ] `.env` file exists in `C:\Clients\FWA\` folder
- [ ] Credentials are correct (test them in Odoo directly)
- [ ] Python can import `xmlrpc.client` (install if missing)

### Step 5: Open in VS Code with Claude Code

```bash
code C:\Clients\FWA
```

Then tell Claude Code:
```
I'm setting up FWA's Odoo automation. 
Read FWA_CLAUDE.md and create a sales order 
for 100 golf shirts for customer "ACME Corp".
```

Claude will orchestrate it!

---

## Core Workflows

### 1. Create a Sales Order
**Who uses this:** Sales team  
**When:** Customer places an order  
**How to request:**
```
Create a sales order:
- Customer: ACME Corporation
- Product: Golf Shirt (blue, size M)
- Quantity: 500
- Delivery date: 2026-02-15
```

### 2. Create a Manufacturing Order
**Who uses this:** Manufacturing lead  
**When:** Need to manufacture golf shirts (CMT subcontracting)  
**How to request:**
```
Create a manufacturing order:
- Product: Golf Shirt - Custom Branding
- Quantity: 500
- Target date: 2026-02-01
```

### 3. Import Inventory
**Who uses this:** Inventory/warehouse team  
**When:** Receive goods or need to adjust stock  
**How to request:**
```
Import inventory from the attached CSV:
- File: stock_levels_jan2026.csv
- Warehouse: Faith Wear Apparel
- Action: Add (or Update)
```

### 4. Process a Purchase Order
**Who uses this:** Procurement team  
**When:** Need to buy fabrics, finished goods, or trims  
**How to request:**
```
Create a purchase order:
- Supplier: ABC Fabrics
- Product: Piqué Knit (white)
- Quantity: 500 meters
- Delivery date: 2026-01-20
```

---

## Key Concepts

### 3-Layer Architecture

**Layer 1: Directives (Instructions)**
- Plain English workflows
- Located in `directives/` folder
- Describe what, not how
- Example: `directives/create_sales_order.md`

**Layer 2: Orchestration (You / Claude)**
- Read the directive
- Validate input from user
- Call the right execution script
- Report back with results

**Layer 3: Execution (Python Scripts)**
- Call Odoo API
- Handle errors
- Return results
- Located in `execution/` folder
- Example: `execution/create_sales_order.py`

### Why This Works

❌ **Bad:** Claude tries to manually navigate Odoo UI  
✅ **Good:** Claude reads a directive, calls a tested script, reports results

Result: **Faster, more reliable, repeatable automation.**

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "xmlrpc.client" import error
```bash
pip install xmlrpc-client
# Or use Python's built-in: python -m xmlrpc.client
```

### "Unable to authenticate"
1. Check `.env` file has correct credentials
2. Test credentials in Odoo directly (login)
3. If using API token, ensure it's not expired
4. Check user has admin or required permissions

### "Product not found in Odoo"
1. Verify product exists in Odoo (`Sales > Products`)
2. Use exact product name or internal ID
3. Ask: "Does the product exist in Odoo?"

### "Field validation error"
1. Check `execution/field_mappings.py` for required fields
2. Ensure all required fields are provided
3. Check field values are correct type (date, number, etc.)

### "Permission denied"
1. Check Odoo user group membership
2. Verify user has access to relevant module (Sales, Manufacturing, etc.)
3. Contact Odoo admin if unsure

---

## Typical Day

### Morning
```
You: "Good morning, show me:
- Sales orders due today
- Low stock items (below 50 units)
- Manufacturing orders in progress"

Claude: [Queries Odoo, generates report]
```

### During Work
```
You: "Create a sales order for 
     500 Golf Shirts (blue) for TechCorp, 
     delivery Feb 15"

Claude: [Reads directive, validates, creates SO, confirms]
Result: ✅ Sales Order #SO-0012345 created
```

### End of Day
```
You: "Import today's stock receipts 
     from the attached file"

Claude: [Validates, imports, alerts if any errors]
Result: ✅ 3 items imported, 1 error (see log)
```

---

## Best Practices

### ✅ Do This
- **Be specific:** "500 golf shirts, size M, blue" (not "lots of shirts")
- **Provide data:** Attach files (CSV, Excel) for bulk operations
- **Verify first:** "Does ABC Fabrics exist as a supplier?" before ordering
- **Check results:** Always verify operation in Odoo afterward
- **Report issues:** If something fails, share the error message

### ❌ Don't Do This
- **Don't assume:** Test with small quantities first (10 units, not 5000)
- **Don't skip validation:** Always confirm product/customer exists first
- **Don't reuse old files:** Use current/updated data files
- **Don't modify .env:** Keep it only for credentials
- **Don't ignore errors:** Understand why something failed before retrying

---

## Getting Help

### If Something Breaks
1. **Check the error message** - copy the full error text
2. **Review the directive** - `directives/[operation].md`
3. **Check the script** - `execution/[script].py`
4. **Look at logs** - `.tmp/audit_logs/` folder
5. **Ask Claude** - Share error + context

### Requesting a New Workflow
If you need a workflow not in `directives/`:
1. Describe the business process clearly
2. List inputs and expected outputs
3. Explain how often you'll use it
4. We'll create the directive + script together

---

## Next Steps

1. **Complete Setup:** Follow "Setup Steps" above
2. **Test Connection:** Run `python execution/odoo_connect.py --test`
3. **Try First Operation:** Create a test sales order
4. **Learn from Results:** Check the audit log, understand what happened
5. **Expand Workflows:** Start using other operations daily

---

## Support Resources

- **Architecture Guide:** Read `FWA_CLAUDE.md` for full system design
- **Specific Workflows:** Check `directives/[operation].md`
- **Field Reference:** See `execution/field_mappings.py` for Odoo fields
- **Odoo Docs:** https://www.odoo.com/documentation
- **FWA Docs:** Check project files for implementation details

---

**Status:** 🟢 Ready for Implementation  
**Last Updated:** 2 January 2026  
**Questions?** Ask Claude in VS Code!
