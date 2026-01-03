# FWA Business Context - Master Reference

## Company Overview

| Field | Value |
|-------|-------|
| **Company** | Faith Wear Apparel (Faith Wear Trading (Pvt) Ltd) |
| **Location** | Harare, Zimbabwe |
| **Founded** | 1997 |
| **Industry** | Branded Apparel Manufacturing & Distribution |
| **Employees** | 5 |
| **Target Market** | Corporate Bespoke Branding and Uniforms (Mid to Large Corporates) |

---

## Odoo Instance

| Field | Value |
|-------|-------|
| **Production URL** | https://fwapparel.odoo.com |
| **Database** | fwapparel |
| **Version** | Odoo 19.0+e (Enterprise) |
| **Go-Live Date** | December 23, 2025 |

---

## Business Model

```
Design → Purchase Materials → Subcontract CMT & Embroidery → Distribute
```

### Revenue Streams
1. **CMT Manufactured Products** - Golf shirts made via Sandy CMT (Zimbabwe)
2. **Imported Finished Goods** - Golf Shirt Fancy from RT Knits (Mauritius)
3. **Purchased Finished Goods** - T-shirts, trousers from local suppliers
4. **Value-Add Services** - Embroidery branding for corporate clients

---

## Products In Scope (Go-Live)

### Finished Goods - CMT Manufactured

| Product | Variants | Supplier |
|---------|----------|----------|
| Golf Shirt Regular Men | 9 colors × 8 sizes = 72 SKUs | Sandy CMT (Zimbabwe) |

### Finished Goods - Imported

| Product | Variants | Supplier |
|---------|----------|----------|
| Golf Shirt Fancy | 6 colors × 6 sizes = 36 SKUs | RT Knits (Mauritius) |

### Future Products (Not in Go-Live Scope)
- T-Shirts (blank) → Printing (DTF/Screen Print)
- Caps (blank) → Optional embroidery
- Trousers (finished goods)
- Bags (finished goods)
- Hoodies
- Woven Shirts
- Aprons

---

## Standard Colors (9)

| Color | Code |
|-------|------|
| White | WHT |
| Black | BLK |
| Red | RED |
| Orange | ORG |
| Navy | NAV |
| Blue | BLU |
| Green | GRN |
| Putty | PUT |
| Mayo | MAY |

---

## Standard Sizes

### Men's (8 sizes)
S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL

### Ladies (6 sizes)
XS, S, M, L, XL, XXL

### Kids - Age Groups (6 sizes)
3-4, 5-6, 7-8, 9-10, 11-12, 13-14

### Trousers - Waist (12 sizes)
28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50

---

## Team Structure

| Code | Name | Role | Order Volume |
|------|------|------|--------------|
| BVR | - | Sales/Operations | 38% of orders |
| MAR | - | Sales/Operations | 24% of orders |
| TAF | - | Sales/Operations | 20% of orders |
| LVR | - | Sales/Operations | 12% of orders |

---

## Legacy System

### "FWA ON THE GO 2025"
- **Format:** Excel spreadsheet
- **Sheets:** 18 tracking sheets
- **Active Orders:** 345 (as of Nov 2025)
- **Key Fields:** Order Number, Company, Contact, Product, Status, Checkboxes

### Process Checkboxes (Replicated in Odoo)
1. ☑ Quotation
2. ☑ Fabric
3. ☑ Manufacturing Order (MO)
4. ☑ Branding
5. ☑ Fiscal
6. ☑ Payment

---

## Key Workflows

### 1. CMT Manufacturing (Golf Shirt Regular)
```
Sales Order → Manufacturing Order → Component Pick → CMT Production → Receive Finished Goods → Deliver
```

### 2. Imported Goods (Golf Shirt Fancy)
```
Purchase Order to RT Knits → Receive Goods → Stock → Sales Order → Deliver
```

### 3. Purchased Finished Goods (T-Shirts, Trousers)
```
Purchase Order to Supplier → Receive Goods → Stock → Sales Order → Deliver
```

### 4. Branding/Embroidery
```
[After manufacturing/receipt] → Send to Embroidery Dave → Receive Branded Goods → Deliver
```

---

## Warehouse Configuration

| Location | Purpose |
|----------|---------|
| WHFWA/Stock | Main finished goods storage |
| WHFWA/Pre-Production | Component staging for CMT |
| WHFWA/Subcontracting | Items at CMT/Embroidery |
| WHFWA/Input | Receiving area |
| WHFWA/Output | Shipping area |

---

## Critical Configuration Notes

### 1. Fabrics as Individual Products
- Each fabric color = separate product (NOT variants)
- Example: `Knit Fabric - Navy 150mm`, `Knit Fabric - Black 150mm`
- Reason: Keeps BOMs simple and consistent

### 2. Finished Goods with Variants
- Use Size variants at finished goods level
- Example: `Golf Shirt Regular Men` with Size: S, M, L, XL, XXL, XXXL

### 3. CMT as Storable Product
- CMT Service must be set up as **Storable Product** (not Service)
- Reason: Required for BOM functionality
- Product Name: `CMT Service - Sandy Zimbabwe`

### 4. Manufacturing over Subcontracting
- Use **Manufacturing** route, NOT Odoo's Subcontracting module
- Reason: 250+ hours testing confirmed SO → MO automation works better this way

---

## Modules Installed

| Module | Status | Purpose |
|--------|--------|---------|
| Sales | ✅ | Quotations, Orders, Customer Management |
| CRM | ✅ | Lead/Opportunity Tracking |
| Inventory | ✅ | Stock, Warehouses, Transfers |
| Purchase | ✅ | Vendor Orders, Subcontracting |
| Manufacturing | ✅ | MO, BOM, Work Orders |
| Accounting | ✅ | Invoicing, Financial Management |
| Website | ✅ | eCommerce (Phase 1) |

---

## Custom Fields (Sales Order)

| Field | Purpose |
|-------|---------|
| Contact Person | Customer contact name |
| Mobile | Contact phone |
| Product | Product description |
| Assigned | Point Man / Staff member |
| Delivery Date | Expected delivery |
| Job Status | Order status |
| Current Handler | Who's working on it now |
| Quotation ✓ | Progress checkbox |
| Fabric ✓ | Progress checkbox |
| MO ✓ | Progress checkbox |
| Branding ✓ | Progress checkbox |
| Fiscal ✓ | Progress checkbox |
| Payment ✓ | Progress checkbox |
| Notes | Special instructions |

---

## Implementation Timeline

| Phase | Date | Status |
|-------|------|--------|
| Demo Instance Setup | Nov 2025 | ✅ Complete |
| Configuration & Testing | Nov-Dec 2025 | ✅ Complete |
| User Training | Dec 2025 | ✅ Complete |
| Go-Live | Dec 23, 2025 | ✅ Live |
| Production Instance | Jan 2026 | 🔄 Current |
| BOM Refinement with CMT | Jan 2026 | 📅 Planned |
| Phase 2 Enhancements | Feb 2026 | 📅 Planned |

---

## Key Files Reference

| File | Location | Purpose |
|------|----------|---------|
| FWA_CLAUDE.md | Root | Agent architecture |
| product_structure_directive.md | directives/ | Product & BOM setup |
| vendors_and_suppliers_directive.md | directives/ | Vendor information |
| FWA_Product_Category_Hierarchy.md | FWA_data/reference-data/ | Full category tree |
| FWA_Staff_Quick_Reference.md | FWA_data/reference-data/ | Staff training guide |

---

## Support Contacts

| Role | Contact |
|------|---------|
| Odoo Admin | Ross Whyte |
| Implementation Partner | TerraForge (terraforge.ai@gmail.com) |

---

## Last Updated
3 January 2026 - Compiled from FWA_data business analysis
