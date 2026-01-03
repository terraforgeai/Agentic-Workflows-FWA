# Status Automation Directive

## Purpose
Define a multi-status tracking system for Sales Orders that automatically updates based on Odoo operations (MO creation, stock moves, pickings, etc.).

**STATUS: PROPOSAL - Awaiting Review**

---

## Problem Statement

Currently, the legacy Excel system tracks orders with:
- One "Status" column trying to capture multiple states
- Manual checkbox updates (Quotation, Fabric, MO, Branding, Fiscal, Payment)
- A "Current Handler" to show where the order physically is

In reality, an order can have **2-3 concurrent states**:
- Overall progress (In Progress, Completed, ON HOLD)
- Physical location (At CMT, At Embroidery, In Warehouse)
- Workflow stage (Awaiting Fabric, In Production, Awaiting Payment)

---

## Proposed Solution: 3 Status Dimensions

### Dimension 1: Order Status (Manual + Some Automation)
**Field:** `x_order_status`
**Purpose:** Overall order lifecycle

| Value | Meaning | Trigger |
|-------|---------|---------|
| `draft` | Order being prepared | Default on creation |
| `in_progress` | Active order | When SO confirmed |
| `on_hold` | Paused (payment issue, stock issue, customer request) | Manual only |
| `ready_delivery` | Complete, ready to ship | All checkboxes ticked |
| `delivered` | Shipped to customer | Delivery picking validated |
| `cancelled` | Order cancelled | SO cancelled |

### Dimension 2: Production Status (Automated)
**Field:** `x_production_status`
**Purpose:** Where is the physical product?

| Value | Meaning | Automation Trigger |
|-------|---------|-------------------|
| `not_started` | No production yet | Default |
| `fabric_on_order` | Fabric PO created | PO created for fabric |
| `fabric_in_stock` | Fabric available | Fabric receipt validated |
| `at_cmt` | At Sandy CMT | MO created/confirmed |
| `at_embroidery` | At Embroidery Dave | Transfer to embroidery location |
| `in_warehouse` | Finished, in stock | MO completed OR receipt validated |
| `dispatched` | Shipped out | Delivery picking validated |

### Dimension 3: Workflow Stage (Checkbox-Driven)
**Field:** `x_workflow_stage`
**Purpose:** What workflow step needs attention?

| Value | Meaning | Derived From |
|-------|---------|--------------|
| `quotation` | Need to send quote | `x_quotation_check` = False |
| `awaiting_fabric` | Need fabric | `x_fabric_check` = False |
| `in_production` | Being manufactured | `x_mo_check` = False |
| `in_branding` | At embroidery/printing | `x_branding_check` = False |
| `awaiting_invoice` | Need to invoice | `x_fiscal_check` = False |
| `awaiting_payment` | Need payment | `x_payment_check` = False |
| `complete` | All done | All checkboxes = True |

---

## Automation Rules (One at a Time)

### Rule 1: Set Production Status when MO Created
**Trigger:** Manufacturing Order (mrp.production) created with origin = SO name
**Action:** Set `x_production_status` = `at_cmt` on linked Sales Order
**Odoo Method:** Automated Action on mrp.production create

### Rule 2: Set Production Status when MO Completed
**Trigger:** Manufacturing Order state changes to `done`
**Action:** Set `x_production_status` = `in_warehouse` on linked Sales Order
**Odoo Method:** Automated Action on mrp.production write (state = done)

### Rule 3: Update Workflow Stage from Checkboxes
**Trigger:** Any x_*_check field changes on Sales Order
**Action:** Compute `x_workflow_stage` based on first False checkbox
**Odoo Method:** Computed field OR Automated Action on sale.order write

### Rule 4: Set Order Status to Delivered
**Trigger:** Delivery picking (stock.picking) validated for this SO
**Action:** Set `x_order_status` = `delivered`
**Odoo Method:** Automated Action on stock.picking write (state = done)

### Rule 5: Set Order Status to Ready for Delivery
**Trigger:** All 6 checkboxes are True
**Action:** Set `x_order_status` = `ready_delivery`
**Odoo Method:** Automated Action on sale.order write

---

## Implementation Approach

**Phase 1: Manual Status Fields (No Automation)**
1. Add the 3 new status fields via Studio
2. Users update manually (like Excel)
3. Validate the field structure works
4. Duration: 1-2 weeks of use

**Phase 2: First Automation (Rule 1 Only)**
1. Implement Rule 1: MO created -> production_status = at_cmt
2. Test with real orders
3. Document any issues
4. Duration: 1 week testing

**Phase 3: Second Automation (Rule 2)**
1. Implement Rule 2: MO done -> production_status = in_warehouse
2. Test with real orders
3. Document any issues

**Phase 4+: Continue one rule at a time**

---

## Fields to Add (Studio)

### New Fields

| Field Label | Technical Name | Type | Default |
|-------------|----------------|------|---------|
| Order Status | `x_order_status` | Selection | `draft` |
| Production Status | `x_production_status` | Selection | `not_started` |
| Workflow Stage | `x_workflow_stage` | Selection | `quotation` |

### Selection Options

**x_order_status:**
```
draft - Draft
in_progress - In Progress
on_hold - ON HOLD
ready_delivery - Ready for Delivery
delivered - Delivered
cancelled - Cancelled
```

**x_production_status:**
```
not_started - Not Started
fabric_on_order - Fabric on Order
fabric_in_stock - Fabric in Stock
at_cmt - At CMT (Sandy)
at_embroidery - At Embroidery (Dave)
in_warehouse - In Warehouse
dispatched - Dispatched
```

**x_workflow_stage:**
```
quotation - Quotation
awaiting_fabric - Awaiting Fabric
in_production - In Production
in_branding - In Branding
awaiting_invoice - Awaiting Invoice
awaiting_payment - Awaiting Payment
complete - Complete
```

---

## Relationship to Existing Fields

### Keep These Fields
| Field | Purpose | Status |
|-------|---------|--------|
| `x_job_status` | Legacy status (backward compatibility) | Keep for now |
| `x_current_handler` | Who has it now | Keep - still useful |
| `x_quotation_check` | Progress checkbox | Keep |
| `x_fabric_check` | Progress checkbox | Keep |
| `x_mo_check` | Progress checkbox | Keep |
| `x_branding_check` | Progress checkbox | Keep |
| `x_fiscal_check` | Progress checkbox | Keep |
| `x_payment_check` | Progress checkbox | Keep |

### Deprecate Later
| Field | Replaced By | When |
|-------|-------------|------|
| `x_job_status` | `x_order_status` + `x_workflow_stage` | After Phase 3 validation |

---

## Visual Layout (Updated FWA on the Go Tab)

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

+-----------------------------------------------------------+
| STATUS                                                    |
+-------------------+-------------------+-------------------+
| Order: [In Prog v]| Production: [CMT v]| Stage: [Fabric v]|
+-------------------+-------------------+-------------------+
| Current Handler: [At CMT (Sandy) v  ]                     |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| PROGRESS                                                  |
+--------+--------+------+--------+--------+--------+
| [x] Qt | [ ] Fb | [ ] MO | [ ] Br | [ ] Fc | [ ] Py |
+--------+--------+------+--------+--------+--------+

+-----------------------------------------------------------+
| NOTES                                                     |
| [                                                       ] |
+-----------------------------------------------------------+
```

---

## Testing Checklist

Before implementing each rule:

- [ ] Document expected behavior
- [ ] Identify test scenarios
- [ ] Create test orders
- [ ] Run automation on test data
- [ ] Verify results
- [ ] Document any edge cases found
- [ ] Get user sign-off
- [ ] Deploy to production
- [ ] Monitor for 1 week
- [ ] Update directive with learnings

---

## Edge Cases to Consider

1. **Order has no MO** (imported finished goods like Golf Shirt Fancy)
   - Production status should skip CMT stages
   - May go directly to `in_warehouse` on receipt

2. **Order cancelled mid-production**
   - What happens to production_status?
   - Should it freeze or reset?

3. **Multiple MOs per SO** (different products on same order)
   - Which MO status takes precedence?
   - May need "partially at CMT" status

4. **Re-work scenario** (goods returned from embroidery)
   - Status goes backward - is this allowed?

5. **Split delivery** (partial shipment)
   - Order status vs line-level status

---

## Decision Required

Before proceeding, please confirm:

1. **Do you approve the 3-dimension status model?**
   - Order Status (lifecycle)
   - Production Status (location)
   - Workflow Stage (what's next)

2. **Do you want to start with Phase 1 (manual fields only)?**

3. **Any changes to the proposed field values?**

---

## Related Files

| File | Purpose |
|------|---------|
| [field_mappings.py](../execution/field_mappings.py) | Will need updates for new fields |
| [fwa_on_the_go_studio_directive.md](fwa_on_the_go_studio_directive.md) | Tab layout reference |
| [fwa_business_context.md](fwa_business_context.md) | Business workflow reference |

---

## Last Updated
3 January 2026 - Initial proposal for review
