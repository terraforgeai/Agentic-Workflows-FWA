# FWA on the Go - Odoo Studio Setup Directive

## Purpose
Configure a custom "FWA on the Go" tab on the Sales Order form in Odoo Studio to replicate the familiar Excel workflow from the legacy "FWA ON THE GO 2025.xlsx" system.

---

## Overview

The FWA team has used an Excel-based tracking system for years. This custom tab brings that workflow into Odoo, maintaining familiarity while gaining ERP integration benefits.

---

## Tab Location

| Setting | Value |
|---------|-------|
| **Model** | Sales Order (sale.order) |
| **Tab Position** | After "Other Info" tab |
| **Tab Name** | FWA on the Go |
| **Tab Icon** | (optional) fa-clipboard-check |

---

## Field Definitions

### Section 1: Order Details

**IMPORTANT: Contact Person Relationship**

The Contact Person field is a **Many2one** link to `res.partner`, NOT a free text field. This ensures:
- Data integrity (no orphaned contact names)
- Contact's phone/mobile is automatically available
- Contacts are properly linked to their parent company

| Field Label | Technical Name | Type | Required | Notes |
|-------------|----------------|------|----------|-------|
| Contact Person | `x_contact_id` | Many2one (res.partner) | No | Linked to company's contacts |
| Mobile | `x_contact_mobile` | Char (Related) | No | Auto-populated from contact |
| Product Description | `x_product_description` | Char | No | Free text product description |
| Assigned (Point Man) | `x_assigned` | Selection | No | Staff member responsible |
| Delivery Date | `x_delivery_date` | Date | No | Expected delivery date |

**Contact Field Domain Filter:**
```python
[('parent_id', '=', partner_id)]
```
This ensures only contacts belonging to the selected customer (company) are shown.

**Mobile Field Configuration:**
- Type: Related Field
- Related: `x_contact_id.mobile`
- Readonly: Yes (auto-populated)

**Assigned Selection Options:**
```
bvr - BVR
mar - MAR
taf - TAF
lvr - LVR
```

---

### Section 2: Job Status

| Field Label | Technical Name | Type | Required | Notes |
|-------------|----------------|------|----------|-------|
| Job Status | `x_job_status` | Selection | No | Current order status |
| Current Handler | `x_current_handler` | Selection | No | Who's working on it now |

**Job Status Selection Options:**
```
in_progress - In Progress
on_hold - ON HOLD
completed - Completed
cancelled - Cancelled
pending_quote - Pending Quote
pending_fabric - Pending Fabric
pending_production - Pending Production
pending_branding - Pending Branding
pending_payment - Pending Payment
ready_delivery - Ready for Delivery
```

**Current Handler Selection Options:**
```
bvr - BVR
mar - MAR
taf - TAF
lvr - LVR
cmt - At CMT (Sandy)
embroidery - At Embroidery (Dave)
warehouse - Warehouse
```

---

### Section 3: Progress Checkboxes

These 6 checkboxes mirror the Excel tracking system. Arrange them **horizontally in a single row** using a group with 6 columns.

| Field Label | Technical Name | Type | Default | Excel Equivalent |
|-------------|----------------|------|---------|------------------|
| Quotation | `x_quotation_check` | Boolean | False | Quotation |
| Fabric | `x_fabric_check` | Boolean | False | Fabric |
| MO | `x_mo_check` | Boolean | False | Making |
| Branding | `x_branding_check` | Boolean | False | Branding |
| Fiscal | `x_fiscal_check` | Boolean | False | Fiscal |
| Payment | `x_payment_check` | Boolean | False | Payment |

**Visual Layout:**
```
+-------------+----------+------+------------+----------+---------+
| [ ] Quote   | [ ] Fab  | [ ] MO | [ ] Brand | [ ] Fisc | [ ] Paid |
+-------------+----------+------+------------+----------+---------+
```

---

### Section 4: Notes

| Field Label | Technical Name | Type | Required | Notes |
|-------------|----------------|------|----------|-------|
| FWA Notes | `x_fwa_notes` | Text | No | Special instructions / comments |

---

## Studio Setup Steps

### Step 1: Access Studio
1. Open any Sales Order in Odoo
2. Click **Toggle Studio** (puzzle piece icon) or press `Ctrl+Shift+S`
3. You're now in Studio edit mode

### Step 2: Add New Tab
1. In the form view, look for the tab bar (where "Order Lines", "Other Info" appear)
2. Click the **+** icon to add a new tab
3. Name it: `FWA on the Go`
4. Drag it to position after "Other Info"

### Step 3: Create Contact Person Field (Many2one)

This is the critical field - must be set up correctly:

1. Click **Add** in the sidebar
2. Select **Many2one** field type
3. Configure:
   - **Label**: Contact Person
   - **Technical Name**: `x_contact_id` (or `contact_id` - Studio adds `x_` prefix)
   - **Model**: `res.partner` (Contacts)
   - **Domain**: `[('parent_id', '=', partner_id)]`

   The domain filter ensures only contacts that are children of the selected customer company are shown.

### Step 4: Create Related Mobile Field

1. Click **Add** in the sidebar
2. Select **Related Field** (or Char with computation)
3. Configure:
   - **Label**: Mobile
   - **Technical Name**: `x_contact_mobile`
   - **Related Field**: `x_contact_id.mobile`
   - **Readonly**: Yes

This field auto-populates when a contact is selected.

### Step 5: Create Remaining Fields

For each remaining field in the tables above:

1. Click **Add** in the sidebar
2. Select the appropriate field type
3. Configure:
   - **Label**: As per "Field Label" column
   - **Technical Name**: As per "Technical Name" column
   - **Required**: As specified
   - For **Selection** fields: Add all options as listed

### Step 6: Arrange Fields in Tab

**Group 1: Order Details**
```
+-----------------------------------------------------------+
| ORDER DETAILS                                             |
+---------------------------+-------------------------------+
| Contact Person: [       ] | Mobile: [              ]      |
+---------------------------+-------------------------------+
| Product Description: [                                  ] |
+---------------------------+-------------------------------+
| Assigned: [BVR v        ] | Delivery Date: [            ] |
+---------------------------+-------------------------------+
```

**Group 2: Job Status**
```
+-----------------------------------------------------------+
| JOB STATUS                                                |
+---------------------------+-------------------------------+
| Job Status: [In Progress v] | Current Handler: [BVR v]   |
+---------------------------+-------------------------------+
```

**Group 3: Progress Checkboxes (6 columns)**
```
+-----------------------------------------------------------+
| PROGRESS                                                  |
+--------+--------+------+--------+--------+--------+
| [ ] Qt | [ ] Fb | [ ] MO | [ ] Br | [ ] Fc | [ ] Py |
+--------+--------+------+--------+--------+--------+
```

**Group 4: Notes**
```
+-----------------------------------------------------------+
| NOTES                                                     |
| [                                                       ] |
| [                                                       ] |
| [                                                       ] |
+-----------------------------------------------------------+
```

### Step 7: Save and Test
1. Click **Close** to exit Studio
2. Create a test Sales Order
3. Select a Customer (company)
4. Navigate to the "FWA on the Go" tab
5. In Contact Person field, verify only contacts from that company appear
6. Select a contact and verify Mobile auto-populates

---

## Data Entry Workflow

### Prerequisite: Contact Setup
Before using the FWA on the Go fields, ensure contacts are properly set up:

1. **Create Company** (if not existing):
   - Go to Contacts
   - Create new contact
   - Check "Is a Company"
   - Fill in company details

2. **Create Contact under Company**:
   - Open the Company contact
   - Click "Contacts & Addresses" tab
   - Add new contact (individual)
   - Fill in Name, Mobile, Email, etc.

### On Sales Order
1. Select Customer (the company)
2. Go to "FWA on the Go" tab
3. Select Contact Person (dropdown shows only contacts under that company)
4. Mobile auto-fills from contact record
5. Fill remaining fields as needed

---

## List View Configuration (Optional)

To show key FWA fields in the Sales Order list view:

1. Open Sales > Orders list view
2. Enter Studio mode
3. Add columns:
   - `x_assigned` (Point Man)
   - `x_job_status` (Status)
   - `x_delivery_date` (Delivery)
4. Consider adding progress checkboxes as icon columns

---

## Search/Filter Configuration (Optional)

Add filters for common searches:

| Filter Name | Field | Operator | Value |
|-------------|-------|----------|-------|
| My Orders (BVR) | x_assigned | = | bvr |
| My Orders (MAR) | x_assigned | = | mar |
| My Orders (TAF) | x_assigned | = | taf |
| My Orders (LVR) | x_assigned | = | lvr |
| In Progress | x_job_status | = | in_progress |
| ON HOLD | x_job_status | = | on_hold |
| Pending Payment | x_payment_check | = | False |

---

## Field Technical Reference

### Full Technical Names (for API/Scripts)
```python
FWA_ON_THE_GO_FIELDS = {
    # Order Details
    'x_contact_id': 'Contact Person (Many2one -> res.partner)',
    'x_contact_mobile': 'Mobile (Related field, readonly)',
    'x_product_description': 'Product Description',
    'x_assigned': 'Assigned (Point Man)',
    'x_delivery_date': 'Delivery Date',

    # Job Status
    'x_job_status': 'Job Status',
    'x_current_handler': 'Current Handler',

    # Progress Checkboxes
    'x_quotation_check': 'Quotation',
    'x_fabric_check': 'Fabric',
    'x_mo_check': 'MO',
    'x_branding_check': 'Branding',
    'x_fiscal_check': 'Fiscal',
    'x_payment_check': 'Payment',

    # Notes
    'x_fwa_notes': 'FWA Notes',
}
```

---

## Migration Notes

When importing legacy data from "FWA ON THE GO 2025.xlsx":

| Excel Column | Odoo Field | Migration Notes |
|--------------|------------|-----------------|
| CompanyName | partner_id | Lookup/create in res.partner |
| Contact | x_contact_id | Lookup/create as child of partner_id |
| Product | x_product_description | Direct mapping |
| PointMan | x_assigned | Map BVR->bvr, MAR->mar, etc. |
| DeliveryDate | x_delivery_date | Date format conversion |
| Status | x_job_status | Map to selection values |
| Quotation | x_quotation_check | Convert to boolean |
| Fabric | x_fabric_check | Convert to boolean |
| Making | x_mo_check | Convert to boolean |
| Branding | x_branding_check | Convert to boolean |
| Fiscal | x_fiscal_check | Convert to boolean |
| Payment | x_payment_check | Convert to boolean |
| Notes | x_fwa_notes | Direct mapping |

**Migration Script Considerations:**
1. First pass: Create/verify all companies in res.partner
2. Second pass: Create contacts under their parent companies
3. Third pass: Create sales orders with proper relationships

---

## Related Files

| File | Purpose |
|------|---------|
| [field_mappings.py](../execution/field_mappings.py) | Python field definitions for API scripts |
| [create_sales_order.py](../execution/create_sales_order.py) | Script to create orders with FWA fields |
| [fwa_business_context.md](fwa_business_context.md) | Business context and workflow reference |

---

## Last Updated
3 January 2026 - Updated to use Many2one contact relationship (no dead data)
