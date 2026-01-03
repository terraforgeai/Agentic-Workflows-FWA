# FWA Odoo Implementation Checklist
## Faith Wear Apparel - Go-Live Readiness Assessment

**Document Version:** 1.0  
**Created:** 2 January 2026  
**Status:** Pre-Implementation  
**Goal:** Validate all systems ready before Claude Code goes live

---

## Overview

This checklist ensures FWA is ready to use the Claude Code automation system for Odoo operations. It covers:
- Odoo configuration (modules, users, data)
- Claude Code setup (Python, credentials, scripts)
- System testing (connection, workflows, error handling)
- Team readiness (training, documentation, support)

---

## Section 1: Odoo Configuration Readiness ✅ / ❌

### Module Installation

- [ ] **Sales Module** - Installed and activated
  - Check: Odoo > Apps > Search "Sales" > Installed
  - Used for: Sales orders, quotations, customer management
  
- [ ] **Manufacturing Module** - Installed and activated
  - Check: Odoo > Apps > Search "Manufacturing" > Installed
  - Used for: Work orders, BOMs, production tracking
  
- [ ] **Inventory Module** - Installed and activated
  - Check: Odoo > Apps > Search "Inventory" > Installed
  - Used for: Stock levels, warehouse management, transfers
  
- [ ] **Purchase Module** - Installed and activated
  - Check: Odoo > Apps > Search "Purchase" > Installed
  - Used for: Purchase orders, supplier management
  
- [ ] **CRM Module** (optional) - Installed and activated
  - Check: Odoo > Apps > Search "CRM" > Installed
  - Used for: Lead management, opportunity tracking

### Users & Permissions

- [ ] **API User Created** - Dedicated Odoo user for automation
  - Name: "Claude Code Automation" or similar
  - Email: automation@company.com
  - Group: Sales, Manufacturing, Inventory, Purchase (all required modules)
  - Note: Should NOT be admin, just enough permissions
  
- [ ] **API Token Generated** - For secure authentication
  - User: Odoo > Settings > Users > [Claude Code user] > API Token
  - Action: Click "Generate Token"
  - Store in: .env file as ODOO_PASSWORD
  
- [ ] **Test User Account** - For validation before production
  - Name: "Test User" or similar
  - Group: Same as API user
  - Purpose: Test workflows without affecting production

- [ ] **Permissions Verified**
  - [ ] Can create sales orders
  - [ ] Can confirm sales orders
  - [ ] Can create manufacturing orders
  - [ ] Can import/create products
  - [ ] Can manage inventory/stock
  - [ ] Can create purchase orders

### Data Setup

#### Customers
- [ ] **Sample Customers Created**
  - [ ] ACME Corporation (for testing)
  - [ ] At least 2-3 real customers
  - Check: Sales > Customers > List
  - Verify: Email, phone, address populated

#### Products
- [ ] **Product Category Hierarchy**
  - Check: Sales > Configuration > Product Categories
  - Must have: Goods/Apparel/[Golf Shirts, T-Shirts, etc.]
  - Must have: Goods/Fabrics/[Knits, Woven]
  - Status: ___ / ___ categories created

- [ ] **Sample Products Created**
  - [ ] Golf Shirt - Blue - Size M (GS-BLUE-M)
  - [ ] T-Shirt - White - Size L (TS-WHITE-L)
  - [ ] Piqué Knit Fabric (white)
  - [ ] At least 5-10 core products
  
  **For each product verify:**
  - [ ] Name clearly described
  - [ ] Internal reference/SKU unique
  - [ ] Category assigned
  - [ ] Unit of measure set
  - [ ] Sales price set
  - [ ] Cost price set

#### BOMs (Bills of Materials)
- [ ] **Golf Shirt BOM Created**
  - Products: Piqué Knit (1.5m), Buttons (4x), Labels (1x), Thread (1 spool)
  - Operations: If using work orders
  - Status: Verified and tested

- [ ] **Manufacturing Instructions**
  - Check: Manufacturing > BOMs > [Golf Shirt]
  - Quantity: 500 units
  - Components show correct fabric consumption (1.5m per unit)

#### Warehouse & Locations
- [ ] **Main Warehouse Configured**
  - Name: "Faith Wear Apparel"
  - Location code: WHFWA
  - Address: 47 Churchill Avenue, Alex Park, Harare

- [ ] **Internal Locations Created**
  - [ ] WHFWA/Stock (main storage)
  - [ ] WHFWA/Pre-Production (component staging)
  - [ ] WHFWA/Subcontracting (if using CMT subcontractors)

- [ ] **Stock Rules Configured**
  - Automatic replenishment rules set
  - Minimum stock thresholds defined
  - Status: ___ rules created

#### Inventory Levels
- [ ] **Initial Stock Imported**
  - Piqué Knit Fabric: ___ meters
  - Golf Shirt - Blue: ___ units
  - Other key products: ___ units each
  - Check: Inventory > Products > Stock

#### Suppliers
- [ ] **Key Suppliers Created**
  - [ ] ABC Fabrics (raw materials)
  - [ ] [Subcontractor name] (CMT manufacturing)
  - [ ] [Other suppliers]
  
  **For each supplier verify:**
  - [ ] Company name
  - [ ] Contact info
  - [ ] Payment terms
  - [ ] Lead time

#### Account Configuration (if doing invoicing)
- [ ] **Chart of Accounts Set Up**
- [ ] **Tax Rates Configured**
- [ ] **Payment Terms Created**

---

## Section 2: Claude Code Setup ✅ / ❌

### Local Environment

- [ ] **Python 3.8+ Installed**
  - Check: `python --version` in terminal
  - Should output: Python 3.8.0 or higher
  
- [ ] **VS Code with Claude Code Extension**
  - Check: VS Code > Extensions > Search "Claude"
  - Install: "Claude" extension from Anthropic
  - Status: Installed and enabled

- [ ] **Required Python Packages**
  - [ ] xmlrpc-client: `pip install xmlrpc-client`
  - [ ] python-dotenv: `pip install python-dotenv`
  - [ ] requests: `pip install requests`
  - Verify: `pip list | grep -E "xmlrpc|dotenv|requests"`

### FWA Project Setup

- [ ] **FWA Directory Created**
  - Location: `/path/to/FWA/`
  - Command: `mkdir FWA && cd FWA`

- [ ] **Core Files in Place**
  - [ ] FWA_CLAUDE.md (architecture guide)
  - [ ] FWA_README.md (quick start)
  - [ ] odoo_connect.py (connection module)
  - [ ] error_handler.py (error handling)
  - [ ] field_mappings.py (data model reference)
  - [ ] create_sales_order.py (execution script)
  - [ ] create_sales_order_directive.md (workflow doc)

- [ ] **.env File Created & Configured**
  - Location: FWA/.env
  - Contents:
    - [ ] ODOO_URL filled in
    - [ ] ODOO_DB filled in
    - [ ] ODOO_USERNAME filled in
    - [ ] ODOO_PASSWORD filled in (use API token)
  - Permissions: Secured (not world-readable)

- [ ] **.gitignore Created**
  - Location: FWA/.gitignore
  - Contents: .env, .tmp/, __pycache__/, *.pyc
  - Purpose: Prevent credential leaks on GitHub

- [ ] **Directories Created**
  - [ ] FWA/.tmp/audit_logs/ (for operation logs)
  - [ ] FWA/.tmp/odoo_exports/ (for exported data)
  - FWA/directives/ (workflow instructions)
  - FWA/execution/ (Python scripts)

---

## Section 3: System Testing ✅ / ❌

### Connection Testing

- [ ] **Odoo Connection Test Passes**
  - Command: `python execution/odoo_connect.py --test`
  - Expected output:
    ```
    ✅ Connected to Odoo [terraforegfwa]
    User: your_email@example.com
    API: Ready
    ```
  - Status: ___PASS___ / ___FAIL___
  - If failed: Check .env credentials

### Execution Script Testing

- [ ] **Sales Order Script Tested**
  - Command: `python execution/create_sales_order.py`
  - Expected: Creates test sales order
  - Verify in Odoo: Sales > Orders > [SO/2026/...]
  - Status: ___PASS___ / ___FAIL___

- [ ] **Test Order Details**
  - Order Reference: ______________
  - Customer: ______________
  - Product: ______________
  - Quantity: ______________
  - Total: ______________

### Workflow Testing

- [ ] **Complete Sales Order Workflow**
  - Step 1: Create SO
  - Step 2: Confirm SO
  - Step 3: Check stock moves
  - Step 4: Manufacturing order created (if applicable)
  - Status: ___PASS___ / ___FAIL___

- [ ] **Error Handling Tested**
  - Test with invalid customer ID
  - Test with insufficient stock
  - Test with invalid product
  - Verify error messages are helpful
  - Status: ___PASS___ / ___FAIL___

- [ ] **Audit Logging Works**
  - Check: FWA/.tmp/audit_logs/
  - Verify logs created for each operation
  - Verify error logs captured
  - Status: ___PASS___ / ___FAIL___

---

## Section 4: Team & Documentation ✅ / ❌

### Training

- [ ] **Sales Team Trained**
  - [ ] How to request a sales order
  - [ ] What information needed (customer, product, qty, date)
  - [ ] Where to find order in Odoo after creation
  - [ ] How to confirm/process order
  - Trainer: ______________
  - Date: ______________

- [ ] **Manufacturing Team Trained**
  - [ ] How to request manufacturing order
  - [ ] How to monitor work orders
  - [ ] How to update production status
  - Trainer: ______________
  - Date: ______________

- [ ] **Inventory/Warehouse Team Trained**
  - [ ] How to import stock levels
  - [ ] How to check stock levels
  - [ ] How to handle stock transfers
  - Trainer: ______________
  - Date: ______________

### Documentation

- [ ] **All Directives Created**
  - [ ] create_sales_order.md ✅ Done
  - [ ] create_manufacturing_order.md (needed)
  - [ ] process_purchase_order.md (needed)
  - [ ] manage_inventory.md (needed)
  - [ ] bulk_import_products.md (needed)
  - [ ] generate_reports.md (needed)

- [ ] **Quick Reference Guides**
  - [ ] Common commands
  - [ ] Error troubleshooting
  - [ ] FAQ
  - [ ] Contact/support info

- [ ] **Field Mappings Documented**
  - Check: execution/field_mappings.py
  - All key models documented:
    - [ ] sale.order
    - [ ] mrp.production
    - [ ] purchase.order
    - [ ] stock.move
    - [ ] product.product
    - [ ] res.partner

### Support Plan

- [ ] **Support Contact Assigned**
  - Name: ______________
  - Email: ______________
  - Phone: ______________
  - Availability: ______________

- [ ] **Escalation Path Defined**
  - Level 1: Check documentation/FAQ
  - Level 2: Contact support person
  - Level 3: Contact Odoo partner/admin
  - Process documented: ___YES___ / ___NO___

- [ ] **Feedback Process**
  - How to request new workflows
  - How to report issues
  - How to suggest improvements
  - Process documented: ___YES___ / ___NO___

---

## Section 5: Security & Compliance ✅ / ❌

### Credential Management

- [ ] **Credentials Secured**
  - [ ] .env file created and secured
  - [ ] API token generated (not using password)
  - [ ] .env NOT in version control
  - [ ] .env NOT shared via email/Slack
  - [ ] File permissions secured (chmod 600 on Linux/Mac)

- [ ] **Access Control**
  - [ ] Only authorized team members have access
  - [ ] API user has minimal permissions (not admin)
  - [ ] Separate test credentials used during development
  - [ ] Production credentials kept separate

### Audit & Logging

- [ ] **Audit Trail Enabled**
  - Check: FWA/.tmp/audit_logs/
  - [ ] Operations logged with timestamps
  - [ ] Errors logged with context
  - [ ] Failed attempts tracked
  - Status: Verified

- [ ] **Log Retention Policy**
  - How long logs kept: ______________
  - Where logs stored: FWA/.tmp/audit_logs/
  - Archive location: ______________
  - Cleanup schedule: ______________

### Change Management

- [ ] **Version Control Setup**
  - [ ] Git repository created (optional)
  - [ ] Sensitive files in .gitignore
  - [ ] Changes tracked with commit messages
  - [ ] Backup strategy in place

- [ ] **Update Process Defined**
  - How directives updated: ______________
  - How scripts updated: ______________
  - Testing before production: ___YES___ / ___NO___
  - Approval process: ______________

---

## Section 6: Go-Live Readiness ✅ / ❌

### Final Checklist

- [ ] All Odoo modules activated and configured
- [ ] All test data imported (customers, products, suppliers)
- [ ] All Odoo permissions set correctly
- [ ] Python environment ready with dependencies
- [ ] FWA directory structure created with all files
- [ ] .env file configured and secured
- [ ] Connection test passes
- [ ] Sales order script tested end-to-end
- [ ] Error handling tested
- [ ] Audit logging verified
- [ ] Team trained on workflows
- [ ] Documentation complete
- [ ] Support process defined
- [ ] Security measures in place
- [ ] Backup strategy confirmed

### Sign-Off

**I confirm that Faith Wear Apparel's Odoo system is ready for Claude Code implementation.**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Odoo Admin | ________________ | __________ | _____________ |
| Implementation Lead | ________________ | __________ | _____________ |
| Sales Lead | ________________ | __________ | _____________ |
| Warehouse Lead | ________________ | __________ | _____________ |

---

## Post-Launch (First Week)

### Daily Checks

- [ ] **Day 1:** Test one complete workflow (create SO, confirm)
- [ ] **Day 2-3:** Run 10-20 transactions, monitor logs
- [ ] **Day 4-5:** Test error scenarios, train team on issues
- [ ] **Day 6-7:** Review audit logs, gather feedback

### Weekly Review

- [ ] All transactions completed successfully: ___%
- [ ] Errors encountered: ____ (list: ____________)
- [ ] Team feedback: ____________
- [ ] Issues to resolve: ____________
- [ ] Updates needed to directives: ___YES___ / ___NO___

### Next Phase Planning

- [ ] Manufacturing order automation ready
- [ ] Purchase order automation ready
- [ ] Inventory bulk import ready
- [ ] Reporting dashboard ready
- [ ] Integration with payment/shipping (if applicable)

---

## Document History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2 Jan 2026 | Initial checklist | Implementation Team |
| | | | |

---

**Status:** 🟡 In Progress  
**Next Step:** Complete Section 1 - Odoo Configuration  
**Target Go-Live:** 2026-01-15

**Questions?** Refer to:
- FWA_CLAUDE.md - System architecture
- FWA_README.md - Quick start guide
- [Specific directive] - For workflow details
