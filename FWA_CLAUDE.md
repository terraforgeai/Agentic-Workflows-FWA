# FWA Agent Instructions
## Faith Wear Apparel - Odoo Implementation & Automation

> **Version:** 1.0  
> **Created:** 2 January 2026  
> **Status:** Live Implementation  
> **Database:** Odoo Online (terraforegfwa)

This file defines how Claude Code operates in VS Code to automate and orchestrate FWA's Odoo instance. It separates concerns into **3 layers** to ensure reliability and consistency.

---

## The 3-Layer Architecture

### Layer 1: Directives (What to do)
- **Location:** `directives/` directory
- **Format:** Markdown SOPs (Standard Operating Procedures)
- **Content:** Goals, inputs, Odoo operations, outputs, edge cases
- **Example:** `directives/create_sales_order.md`, `directives/manufacture_work_order.md`
- These describe *what* needs to happen in plain English

### Layer 2: Orchestration (Decision making & routing)
- **This is you.** Claude in VS Code.
- **Your job:** Read directives → understand business logic → call execution scripts in correct order
- **Handle:** Error recovery, clarifications, directive updates
- **Example:** User says "Create a sales order for 500 golf shirts" → you read `directives/create_sales_order.md` → call `execution/create_sales_order.py` with validated inputs
- You're the bridge between human intent and deterministic Odoo operations

### Layer 3: Execution (Doing the work)
- **Location:** `execution/` directory
- **Format:** Python scripts using Odoo RPC API
- **Responsibility:** API calls, data validation, transformations, error handling
- **Examples:**
  - `execution/odoo_connect.py` - Connection management
  - `execution/create_sales_order.py` - Create SO in Odoo
  - `execution/manufacture_work_order.py` - Create MO in Odoo
  - `execution/bulk_inventory_import.py` - Import stock levels
  - `execution/generate_bom_report.py` - Extract BOM data

**Why this works:** LLMs are probabilistic, Odoo operations are deterministic. Push complexity into Python → you focus on intelligent decision-making.

---

## Core Operating Principles

### 1. Check execution scripts first
Before doing anything manually, check if a script exists in `execution/`:
- ✅ If script exists → use it (faster, reliable)
- ❌ If script doesn't exist → ask user permission before creating new one
- Always prefer existing tools over writing new code

### 2. Self-anneal when errors occur
When something breaks:
1. **Read** the error message and Odoo API response
2. **Fix** the script (Odoo authentication, field mappings, validation rules)
3. **Test** locally before running on live data
4. **Update** the directive with what you learned
5. **Document** API limits, field requirements, timing expectations

Example: You hit an Odoo field validation error → check field type in Odoo docs → update script validation → update directive → system stronger

### 3. Update directives as you learn
Directives are **living documents**. When you discover:
- Odoo field requirements or constraints
- API rate limits or pagination
- Common errors or workarounds
- Better workflows
- Data dependencies

→ Update the directive to include this learning

### 4. Validate data before pushing to Odoo
Always ensure:
- Required fields are present
- Field values match Odoo field types (string, integer, float, date, selection, many2one, etc.)
- References to other records (customers, products, warehouses) exist in Odoo
- Quantities, prices, dates are reasonable (catch obvious errors)

---

## File Organization

### Directory Structure
```
C:\Clients\FWA\                    # Root project directory (PRODUCTION)
├── .env                           # Environment variables (Odoo credentials)
├── FWA_CLAUDE.md                  # This file - architecture & principles
├── FWA_README.md                  # Quick start guide
├── INDEX.md                       # Complete documentation index
├── QUICK_REFERENCE.md             # One-page daily reference
├── IMPLEMENTATION_CHECKLIST.md    # Go-live verification
├── DELIVERABLES_SUMMARY.md        # Overview of all deliverables
│
├── directives\                    # Layer 1: SOPs in Markdown
│   ├── create_sales_order_directive.md
│   ├── create_manufacturing_order_directive.md
│   ├── process_purchase_order_directive.md
│   ├── manage_inventory_directive.md
│   ├── bulk_import_products_directive.md
│   ├── generate_reports_directive.md
│   └── ... (one per workflow)
│
├── execution\                     # Layer 3: Deterministic Python scripts
│   ├── __init__.py                # Python package marker
│   ├── odoo_connect.py            # Connection & auth (FOUNDATIONAL)
│   ├── error_handler.py           # Standardized error handling
│   ├── field_mappings.py          # Odoo field definitions (data model reference)
│   ├── create_sales_order.py      # Sample execution script
│   ├── create_manufacturing_order.py
│   ├── process_purchase_order.py
│   ├── bulk_inventory_import.py
│   ├── generate_reports.py
│   └── ... (one per major operation)
│
├── .tmp\                          # Temporary files (auto-generated, never commit)
│   ├── odoo_exports\              # Exported data for processing
│   ├── audit_logs\                # Execution logs & errors
│   │   ├── operations_20260102.log
│   │   ├── audit_20260102.jsonl
│   │   └── ...
│   └── ... (regenerated each session)
│
└── .gitignore                     # Git ignore file
    # Contents:
    # .env
    # .tmp/
    # __pycache__/
    # *.pyc
```

**Note:** All paths above use Windows format relative to `C:\Clients\FWA\` as your root directory.

### Key Principle: Local vs Cloud
- **Local files** (`.tmp/`, `execution/`, `directives/`) = Processing & orchestration
- **Cloud outputs** = None currently; can add Google Sheets exports if needed
- Everything in `.tmp/` can be deleted and regenerated

---

## Odoo Connection & Authentication

### .env File (REQUIRED)
```
# Odoo Online Credentials
ODOO_URL=https://fwapparel.odoo.com
ODOO_DB=fwapparel
ODOO_USERNAME=fwapparel@protonmail.com
ODOO_PASSWORD=your_password_or_api_token
ODOO_API_KEY=8bd5907511c8d3c51aa488386952c24552ef76e3

# Execution Logging
LOG_LEVEL=INFO
LOG_PATH=.tmp/audit_logs/
```

**⚠️ Security Note:** Never commit `.env` to version control. Use `.gitignore`:
```
.env
.tmp/
__pycache__/
*.pyc
```

### Connection Testing
Before running any workflow:
```bash
# From VS Code terminal
python execution/odoo_connect.py --test
# Should output: ✅ Connected to Odoo [database name]
```

---

## FWA Core Workflows

### Workflow 1: Sales → Manufacturing (CMT Subcontracting)
**Trigger:** Customer orders golf shirts with custom branding

**Steps:**
1. User creates sales order in Odoo (or you create via script)
2. Read `directives/create_sales_order.md`
3. Call `execution/create_sales_order.py` 
4. Confirm order created in Odoo
5. Manufacturing order automatically created (if configured)
6. Update `directives/create_manufacturing_order.md` with any learnings

**Expected Odoo changes:**
- Sales Order created in `sale.order`
- Manufacturing Order in `mrp.production` (if MTO enabled)
- Material Shortage Report (if stock insufficient)

---

### Workflow 2: Purchase Order Management
**Trigger:** Need to order finished goods (caps, t-shirts) or raw materials (fabrics, labels)

**Steps:**
1. Read `directives/process_purchase_order.md`
2. Call `execution/process_purchase_order.py` with supplier & product details
3. Confirm PO created in Odoo
4. Receive goods → inventory updated
5. Manage subcontracting operations (if applicable)

---

### Workflow 3: Inventory & Warehouse Operations
**Trigger:** Stock receipts, transfers, quality checks, location management

**Steps:**
1. Read `directives/manage_inventory.md`
2. Call `execution/bulk_inventory_import.py` (if bulk import) OR manual entry
3. Validate stock levels in correct locations (Stock, Pre-Production, Subcontracting)
4. Generate reports on low stock, variances, or aging inventory

**Multi-location complexity:**
- `WHFWA/Stock` - Main storage
- `WHFWA/Pre-Production` - Component staging
- `WHFWA/Subcontracting` - In-transit to/from subcontractors

---

### Workflow 4: Manufacturing & Work Orders
**Trigger:** Need to manufacture golf shirts or other assembled products

**Steps:**
1. Read `directives/create_manufacturing_order.md`
2. Call `execution/create_manufacturing_order.py` with BOM & quantities
3. Odoo creates work order with:
   - Components to pick
   - Operations assigned
   - Quality checks configured
4. Manufacturing worker scans components, completes operations
5. System tracks fabric consumption (1.5m per garment standard)
6. Finished goods move to stock

---

## Error Handling & Self-Annealing

### When Something Breaks

**Scenario 1: Odoo API Authentication Error**
```
Error: [EACCES] Unable to authenticate user
```
Action:
1. Check `.env` credentials are correct
2. Verify API token is valid (Odoo expires tokens)
3. Update `execution/error_handler.py` with retry logic
4. Update `directives/troubleshooting.md` with this solution

**Scenario 2: Field Validation Error**
```
Error: Field 'partner_id' missing or invalid value
```
Action:
1. Check script: does it include the required field?
2. Check Odoo data model: is the customer created first?
3. Add validation in `execution/field_mappings.py`
4. Update directive with field requirements

**Scenario 3: Data Not Found**
```
Error: Product 'Golf Shirt - Blue - Size M' does not exist
```
Action:
1. Check script: is it looking up product correctly?
2. Check Odoo: does the product exist with exact name/SKU?
3. Update script to use product_id instead of name if IDs are more reliable
4. Document in directive: "Always use internal product IDs, not display names"

### General Recovery Loop
```
User request
    ↓
Read directive
    ↓
Validate inputs
    ↓
Call execution script
    ↓
Error? → Fix script → Test → Update directive → Re-run
    ↓
Success → Log operation → Return results
```

---

## Directive Template

When creating a new directive, use this structure:

```markdown
# [Operation Name] Directive

## Purpose
What does this workflow accomplish?

## Inputs
- Parameter 1 (type, required/optional, example)
- Parameter 2 (type, required/optional, example)
- ...

## Prerequisites
- [ ] Odoo connection active
- [ ] User has permissions for [module]
- [ ] [Resource] exists in Odoo
- ...

## Steps
1. Validate inputs (type checking, data existence)
2. Check Odoo for conflicts (duplicate records, invalid references)
3. Create/update record in Odoo
4. Confirm changes
5. Return record ID and key data

## Outputs
- Success: Record ID, summary of changes
- Failure: Error message, recommended action

## Edge Cases
- What if [resource] already exists?
- What if required field is missing?
- What if user lacks permissions?

## Odoo Modules Involved
- [Module] (e.g., sale, manufacture, inventory)

## Related Scripts
- execution/[script].py

## Last Updated
[Date] - [What changed]
```

---

## Execution Script Template

When creating a new execution script, use this structure:

```python
#!/usr/bin/env python3
"""
[Operation Name] - Deterministic Odoo Operation

Purpose: [What does this script do?]
Input: [What parameters does it expect?]
Output: [What does it return?]

Related Directive: directives/[directive_name].md
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

# Import shared modules
from odoo_connect import OdooConnection
from error_handler import handle_error, log_operation
from field_mappings import FIELD_DEFINITIONS

# Setup logging
logger = logging.getLogger(__name__)

def main(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function.
    
    Args:
        input_params: Dictionary with required parameters
    
    Returns:
        Dictionary with operation result (success/failure, data, messages)
    """
    try:
        # 1. Validate inputs
        validate_inputs(input_params)
        
        # 2. Connect to Odoo
        odoo = OdooConnection()
        
        # 3. Execute operation
        result = perform_operation(odoo, input_params)
        
        # 4. Log success
        log_operation('SUCCESS', result)
        
        return {
            'status': 'success',
            'data': result,
            'message': 'Operation completed'
        }
    
    except Exception as e:
        error_response = handle_error(e)
        log_operation('ERROR', error_response)
        return error_response

def validate_inputs(params: Dict[str, Any]) -> None:
    """Validate all required inputs."""
    # Add validation logic
    pass

def perform_operation(odoo: OdooConnection, params: Dict[str, Any]) -> Any:
    """Execute the core Odoo operation."""
    # Add operation logic
    pass

if __name__ == '__main__':
    # For CLI testing
    test_input = {
        # Example inputs
    }
    result = main(test_input)
    print(json.dumps(result, indent=2, default=str))
```

---

## Checklist: Before Go-Live

Use this to validate the system is ready:

- [ ] **Odoo Connection**
  - [ ] `.env` file has correct credentials
  - [ ] `python execution/odoo_connect.py --test` passes
  - [ ] API key/token valid and non-expired

- [ ] **Core Scripts Exist**
  - [ ] `execution/create_sales_order.py` - tested with real customer data
  - [ ] `execution/create_manufacturing_order.py` - tested with real BOM
  - [ ] `execution/process_purchase_order.py` - tested with real supplier
  - [ ] `execution/bulk_inventory_import.py` - tested with real stock data

- [ ] **Directives Complete**
  - [ ] All 4 core workflows documented
  - [ ] Edge cases covered
  - [ ] Last Updated date current

- [ ] **Data Quality**
  - [ ] All customers exist in Odoo
  - [ ] All products exist with correct BOMs
  - [ ] All suppliers configured
  - [ ] All warehouse locations created
  - [ ] All stock rules configured

- [ ] **Error Handling**
  - [ ] `execution/error_handler.py` handles common Odoo errors
  - [ ] Scripts log operations to `.tmp/audit_logs/`
  - [ ] Critical errors create alerts (optional: email/Slack)

- [ ] **Team Training**
  - [ ] Sales team knows how to request SO creation
  - [ ] Manufacturing team knows how to request MO creation
  - [ ] Inventory team knows how to bulk import stock
  - [ ] Everyone knows troubleshooting procedure

---

## Quick Start

### 1. Initial Setup (One-time)
```bash
# Navigate to your FWA directory
cd C:\Clients\FWA

# Create .env file with your Odoo credentials
# (Copy from .env.template and fill in your credentials)
# Edit with: ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD

# Test connection
python execution/odoo_connect.py --test
```

### 2. Daily Workflow
```bash
# Open FWA directory in VS Code
code C:\Clients\FWA

# In Claude Code, tell me what you need:
# "Create a sales order for 500 golf shirts for ACME Corp"
# "Bulk import inventory from the attached file"
# "Generate a manufacturing schedule for next week"

# I'll:
# 1. Read the relevant directive
# 2. Validate your input
# 3. Call the execution script
# 4. Confirm changes in Odoo
# 5. Report results
```

### 3. Ongoing Maintenance
- Check `.tmp/audit_logs/` weekly for errors
- Update directives as business processes evolve
- Keep execution scripts version-controlled
- Test any new scripts with test data first

---

## Odoo Modules at a Glance

| Module | Purpose | Key Records | Status |
|--------|---------|-------------|--------|
| **CRM** | Lead/opportunity management | Leads, opportunities | Phase 1 ✅ |
| **Sales** | Customer orders, quotations | Sale Orders, Quotations | Phase 1 ✅ |
| **Purchase** | Supplier orders, subcontracting | Purchase Orders, RFQs | Phase 1 ✅ |
| **Manufacturing** | Work orders, BOMs | MO, BOM, Operations | Phase 1 ✅ |
| **Inventory** | Stock, locations, transfers | Stock Moves, Lots | Phase 1 ✅ |
| **Website** | eCommerce, online catalog | Website, products | Phase 1 ✅ |
| **Accounting** | Invoices, journals, GL | Invoices, bills | Phase 2 🔲 |
| **Employees** | HR, payroll | Employee records | Phase 2 🔲 |

---

## Support & Troubleshooting

### Common Issues

**Issue: "Module not installed"**
- Check `directives/troubleshooting.md` for module installation steps
- Confirm with Odoo admin that module is activated

**Issue: "Permission denied"**
- Odoo user needs permissions for the operation
- Check user group assignments in Odoo Settings

**Issue: "Field not found"**
- Script might reference outdated field name
- Check `execution/field_mappings.py` for current field definitions
- Update script and directive if field changed

**Issue: "Rate limit exceeded"**
- Odoo API might be throttling requests
- Add delays between bulk operations
- Document in directive: "Allow 1-2 second delay between 100+ records"

### Getting Help
1. Check relevant directive (`directives/[operation].md`)
2. Review execution script (`execution/[script].py`)
3. Check error logs (`.tmp/audit_logs/`)
4. Look up field definitions (`execution/field_mappings.py`)
5. Ask for clarification in your request

---

## Document Versions & History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2 Jan 2026 | Initial FWA implementation structure |

---

**Status:** 🟢 Ready for Phase 1 Go-Live Implementation  
**Last Updated:** 2 January 2026  
**Next Review:** Post-launch debrief
