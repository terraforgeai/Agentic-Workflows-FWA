# FWA ODOO IMPLEMENTATION GUIDE
## Product Setup & Data Loading Instructions
**Go-Live Date:** Monday, December 23, 2025

---

## TABLE OF CONTENTS
1. Odoo Module Requirements
2. Product Attribute Setup
3. Product Category Loading
4. Product Creation Workflow
5. BOM Configuration (CMT Products)
6. Sales Order Configuration
7. Staff Training Focus Areas
8. Go-Live Checklist

---

## 1. ODOO MODULE REQUIREMENTS

**Required Modules:**
- [x] Sales
- [x] Inventory
- [x] Manufacturing (for BOMs/CMT)
- [x] Purchase (for supplier management)
- [x] Accounting (Chart of Accounts)
- [x] Website (if using portal)

**Recommended Modules:**
- [ ] Product Matrix (for color/size variant visualization)
- [ ] Advanced Inventory
- [ ] Manufacturing MRP

---

## 2. PRODUCT ATTRIBUTE SETUP

### Step 1: Create Color Attribute

**Path:** Inventory > Products > Attributes

| Field | Value |
|-------|-------|
| Attribute Name | Color |
| Create Variants | Yes (✓) |
| Values (Create) | White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo |

### Step 2: Create Size Attributes

**Size - Men (for Golf Shirts, T-Shirts, Woven, Hoodies)**

| Field | Value |
|-------|-------|
| Attribute Name | Size Men |
| Create Variants | Yes (✓) |
| Values | S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL |

**Size - Ladies**

| Field | Value |
|-------|-------|
| Attribute Name | Size Ladies |
| Create Variants | Yes (✓) |
| Values | XS, S, M, L, XL, XXL |

**Size - Kids (Age Groups)**

| Field | Value |
|-------|-------|
| Attribute Name | Size Kids |
| Create Variants | Yes (✓) |
| Values | 3-4, 5-6, 7-8, 9-10, 11-12, 13-14 |

**Size - Trousers (Waist)**

| Field | Value |
|-------|-------|
| Attribute Name | Waist |
| Create Variants | Yes (✓) |
| Values | 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50 |

### Step 3: Confirm Attribute Order (Optional)

Set sequence for variant display:
1. Color (Sequence: 1)
2. Size (Sequence: 2)

This ensures variants appear as Color first, then Size.

---

## 3. PRODUCT CATEGORY LOADING

### Import Method: Two Options

#### OPTION A: Manual Creation (Good for understanding structure)
1. Go to: **Inventory > Products > Categories**
2. Create each category manually
3. Select Parent Category as you go

#### OPTION B: CSV Bulk Import (Faster)
1. Prepare CSV with columns:
   - `Name` (Category display name)
   - `Parent Category/Name` (Parent category name)
   - `Type` (Normal, View)
   - `Sequence` (order)

2. Go to: **Inventory > Products > Categories**
3. Click **Import**
4. Upload CSV file
5. Map columns to Odoo fields

### Category CSV Structure

```
Name,Parent Category/Name,Type,Sequence,Description
Goods,,View,1,Finished Goods - Locally Sourced
Finished Goods,Goods,Normal,1,All locally finished goods
Accessories,Finished Goods,Normal,1,Caps and Bags
Caps,Accessories,Normal,1,Regular caps - Local ZW and Imported variants
Bags,Accessories,Normal,2,Travel Bag and GYM Bag
Bottoms,Finished Goods,Normal,2,Trousers and Tracksuit Bottoms
Trousers,Bottoms,Normal,1,Slim Fit Trousers
Tracksuit Bottoms,Bottoms,Normal,2,Men and Ladies tracksuit bottoms
Outerwear,Finished Goods,Normal,3,Hoodies and Winter Range
Hoodies,Outerwear,Normal,1,Brushed Knitwear variants
Tops,Finished Goods,Normal,4,Golf Shirts T-Shirts Woven Shirts Kids Aprons
Golf Shirts Local CMT,Tops,Normal,1,CMT Manufactured Golf Shirts Regular
T-Shirts,Tops,Normal,2,Purchased T-Shirts
Woven Shirts,Tops,Normal,3,Short and Long Sleeve Woven Shirts
Kids T-Shirts,Tops,Normal,4,Kids apparel
Tracksuit Tops,Tops,Normal,5,Men and Ladies tracksuit tops
Aprons,Tops,Normal,6,Chambre Denim and variants
Imported Goods,,View,2,Finished Goods - Imported
Golf Shirts Fancy,Imported Goods,Normal,1,Premium Imported Golf Shirts
Caps Imported,Imported Goods,Normal,2,Imported Trucker Cap variants
Raw Material,,View,3,Raw Materials - Locally Sourced
Fabrics,Raw Material,Normal,1,Knit and Woven fabrics
Knits,Fabrics,Normal,1,Knit fabrics by color and width
Trims,Raw Material,Normal,2,Labels Buttons Thread
Labels,Trims,Normal,1,FWA Labels
Raw Material Imports,,View,4,Raw Materials - Imported
Imported Fabrics,Raw Material Imports,Normal,1,Imported fabrics
Imported Trims,Raw Material Imports,Normal,2,Imported trims
Services,,View,5,Manufacturing and Value-Add Services
CMT,Services,Normal,1,Cut Make Trim Services
Embroidery,Services,Normal,2,Embroidery Services
Printing,Services,Normal,3,Printing Services
```

**Save as:** `FWA_Product_Categories.csv`

---

## 4. PRODUCT CREATION WORKFLOW

### Finished Goods Template

**Product Type:** Storable Product / Product with Variants

#### EXAMPLE: Golf Shirt Regular Men

| Field | Value |
|-------|-------|
| **Product Name** | Golf Shirt Regular Men |
| **Internal Reference** | GSM-001 |
| **Category** | Golf Shirts Local CMT |
| **Product Type** | Storable Product |
| **Can be Sold** | Yes ✓ |
| **Can be Purchased** | No ✗ |
| **Attributes** | Color, Size Men |
| **Unit of Measure** | Units (piece) |
| **Sales Price** | *To be entered per variant or as base* |
| **Cost** | *To be calculated from BOM* |

**Variants Generated:** 9 colors × 8 sizes = 72 variants automatically

#### EXAMPLE: T-Shirt Regular Round Neck (Purchased)

| Field | Value |
|-------|-------|
| **Product Name** | T-Shirt Regular Round Neck |
| **Internal Reference** | TSR-001 |
| **Category** | T-Shirts |
| **Product Type** | Storable Product |
| **Can be Sold** | Yes ✓ |
| **Can be Purchased** | Yes ✓ |
| **Attributes** | Color, Size Men (or Size Ladies/Kids per variant) |
| **Supplier(s)** | African Threads, Kutaura Enterprises |
| **Unit of Measure** | Units (piece) |

#### EXAMPLE: Trousers Slim Fit (Purchased by Waist)

| Field | Value |
|-------|-------|
| **Product Name** | Trousers Slim Fit |
| **Internal Reference** | TSF-001 |
| **Category** | Trousers |
| **Product Type** | Storable Product |
| **Can be Sold** | Yes ✓ |
| **Can be Purchased** | Yes ✓ |
| **Attributes** | Color, Waist (Size) |
| **Supplier(s)** | Paramount Garments Works |
| **Unit of Measure** | Units (piece) |

**Variants Generated:** 9 colors × 12 waists = 108 variants

#### EXAMPLE: Raw Material - Knit Fabric

| Field | Value |
|-------|-------|
| **Product Name** | Knit Fabric - Navy 150mm |
| **Internal Reference** | KF-NAV-150 |
| **Category** | Knits |
| **Product Type** | Storable Product |
| **Can be Sold** | No ✗ |
| **Can be Purchased** | Yes ✓ |
| **Attributes** | None (individual fabric per color/width) |
| **Supplier(s)** | *To be confirmed* |
| **Unit of Measure** | Meters |
| **Weight:** | *GSM to be added* |

**Note:** Create separate products for each color/width combination:
- Knit Fabric - White 150mm
- Knit Fabric - Black 150mm
- Knit Fabric - Navy 150mm
- ... (continue for all 9 colors)

---

## 5. BOM CONFIGURATION (CMT PRODUCTS)

### Golf Shirt Regular Men - BOM Setup

**Path:** Manufacturing > Master Data > Bills of Material

| Field | Value |
|-------|-------|
| **Product** | Golf Shirt Regular Men |
| **Product Qty** | 1 |
| **Unit of Measure** | Units (piece) |
| **Type** | Normal (produce this product) |
| **Picking Type** | Pick components and produce |

### BOM Line Components

| Component | Quantity | Unit | Notes |
|-----------|----------|------|-------|
| Knit Fabric 150mm* | *TBD* | Meters | *Confirmed with CMT in Jan 2026* |
| FWA Label | 1 | Piece | CMT-supplied; appears in BOM for tracking |
| Buttons** | *TBD* | Piece | CMT-supplied |
| Sewing Thread** | *TBD* | Meters | CMT-supplied |

**IMPORTANT NOTES:**

*\* Knit Fabric 150mm:* This is a placeholder/generic component. Staff can substitute any knit fabric color (Navy, Black, White, etc.) as long as width = 150mm. Consumption quantity should be based on actual meter requirement per shirt size.

**\*\* CMT-Supplied Items:** Buttons and thread are supplied by CMT. How to handle in Odoo:
- **Option 1:** Track in BOM but with zero cost (informational)
- **Option 2:** Don't include in BOM; track in CMT service record
- **Recommendation:** Option 1 (for full visibility of all components)

### Fabric Width Changes

**If fabric width changes (e.g., 160mm instead of 150mm):**
1. Create new product: "Golf Shirt Regular Men - 160mm"
2. Create separate BOM with updated consumption
3. Different consumption rate required = different BOM

---

## 6. SALES ORDER CONFIGURATION

### Critical: Color + Size Capture

**Default Sales Order Line Format (MAY NEED CUSTOMIZATION)**

Standard Odoo shows:
```
Product | Quantity | Unit Price | Subtotal
```

**FWA Requirement:**
```
Product | Color | Size | Quantity | Unit Price | Subtotal
```

### Implementation Steps

#### Option A: Use Product Variants (Standard)
1. Product variants are automatically created when you add Color + Size attributes
2. In Sales Order, select specific variant (e.g., "Golf Shirt Regular Men - Navy-L")
3. This automatically captures color and size

**Advantage:** Clean, standard Odoo workflow
**Limitation:** User must select from variant list (can be long with 72+ variants)

#### Option B: Product Matrix View (Better UX)
1. Install: **Product Matrix** module (if available in your Odoo version)
2. On Sales Order line, color/size appear as grid
3. User clicks Navy-L directly
4. Much faster for apparel businesses

#### Option C: Custom Fields (Most Transparent)
1. Add custom fields to Sales Order Line:
   - Color (Selection field)
   - Size (Selection field)
2. Require product to be "Product with Variants"
3. Display all three clearly in print/reports

**Recommendation:** Option B (Product Matrix) if available; otherwise Option A

### Sample Sales Order Report

**What the printed Sales Order should show:**

```
FAITH WEAR APPAREL SALES ORDER

Customer: XYZ Company
Order Date: December 20, 2025

Line | Product | Color | Size | Quantity | Unit Price | Total
-----|---------|-------|------|----------|------------|-------
1    | Golf Shirt Regular Men | Navy | L | 100 | $8.50 | $850.00
2    | Golf Shirt Regular Men | White | M | 150 | $8.50 | $1,275.00
3    | T-Shirt Regular Round Neck | Black | S | 50 | $5.00 | $250.00
4    | Trousers Slim Fit | Navy | 34 | 75 | $12.00 | $900.00
```

---

## 7. STAFF TRAINING FOCUS AREAS

### 1. Product Management Team Training

**Topics to Cover:**

**A) Understanding the Category Structure**
- Why we have Root categories (Goods, Imported, Raw Materials, Services)
- How to navigate the tree to find products
- When to add new products vs. new variants

**B) Fabric Management & BOM Flexibility**
- Each fabric = separate product (Knit Fabric - Navy 150mm, etc.)
- NO color variants within fabric products
- Why this simplifies BOMs
- How width changes affect BOMs

**C) Variant Management**
- Color + Size variants are created AUTOMATICALLY when you set attributes on finished goods
- Do NOT manually create variant products
- How to set variant prices (if they differ)

**D) Sales Order Entry**
- How to select color + size when creating sales orders
- Why this is critical for production planning
- How to read the variant reference
- How to interpret variant SKU

**E) CMT Production Planning**
- How BOMs work for CMT Golf Shirts
- Fabric substitution rules (width must stay 150mm)
- How to handle fabric changes in Odoo
- When to create new BOM

### 2. Warehouse/Inventory Team Training

**Topics:**
- Receiving goods with color and size variants
- Bin location strategy for variants
- Stock levels per color/size
- Picking and packing by color/size for orders
- How to generate picking lists that show color/size clearly

### 3. Sales Team Training

**Topics:**
- How to quote with color and size variants
- How to clearly communicate color/size to customers
- Using the product matrix for fast variant selection
- How color/size appears on sales orders and confirmations

### 4. Finance/Accounting Team Training

**Topics:**
- Cost calculation for variants (if different)
- How BOMs feed into standard costing
- Pricing strategy for color variants (if different)
- Reporting by product, color, size

---

## 8. GO-LIVE CHECKLIST

### PRE-GO-LIVE (Friday & Saturday)

**Product Setup:**
- [ ] Product Attributes created (Color, Size Men, Size Ladies, Size Kids, Waist)
- [ ] All Product Categories loaded into Odoo
- [ ] Finished goods products created with variants
- [ ] Raw material products created (fabrics by color/width)
- [ ] BOMs configured for CMT products (Golf Shirt Regular Men)

**Data Validation:**
- [ ] Verify all 72 variants created for Golf Shirt Regular Men
- [ ] Check variant pricing (if applicable)
- [ ] Confirm BOM component quantities
- [ ] Verify supplier information is complete
- [ ] Review internal reference codes (SKUs)

**System Configuration:**
- [ ] Sales order print layout configured to show Color + Size
- [ ] Stock locations set up (optional: by color/size)
- [ ] User permissions set for each department
- [ ] Dashboard configured for daily monitoring

**Training:**
- [ ] Product management team trained
- [ ] Warehouse team trained
- [ ] Sales team trained
- [ ] Finance team trained

**Documentation:**
- [ ] Product reference guide distributed to staff
- [ ] How-to guides for common tasks posted
- [ ] Escalation contact list created

### GO-LIVE DAY (Monday)

**Pre-Go-Live:**
- [ ] Final system check (all products active)
- [ ] Test sales order workflow with color/size
- [ ] Confirm all staff can access their dashboards
- [ ] Backup database created

**During Go-Live:**
- [ ] Monitor first sales orders
- [ ] Check production picking lists
- [ ] Verify inventory counts match expected
- [ ] Resolve any variant selection issues
- [ ] Monitor user activity logs for errors

**Post Go-Live (First Week):**
- [ ] Daily check-ins with department heads
- [ ] Gather feedback on pain points
- [ ] Monitor order accuracy (color/size)
- [ ] Adjust workflows as needed
- [ ] Plan for January 2026 BOM refinement with CMT

### POST-GO-LIVE (January 2026)

- [ ] Collaborate with CMT on fabric consumption validation
- [ ] Refine and finalize BOMs with actual production data
- [ ] Confirm supplier details for TBD products
- [ ] Train on any process adjustments
- [ ] Plan for expansion of product lines (Aprons, etc.)

---

## QUICK REFERENCE: PRODUCT CREATION EXAMPLES

### Example 1: Finished Good with Variants

**Product:** T-Shirt Regular Round Neck

```
Name: T-Shirt Regular Round Neck
Category: T-Shirts
Can be Sold: Yes
Can be Purchased: Yes
Attributes to Assign: Color, Size Men
Attributes: {Color: [White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo],
             Size Men: [S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL]}

Result: 9 colors × 8 sizes = 72 variants created automatically
Example variant names:
- T-Shirt Regular Round Neck - White-S
- T-Shirt Regular Round Neck - Navy-XL
- T-Shirt Regular Round Neck - Black-XXXXL
```

### Example 2: Raw Material (No Variants)

**Product:** Knit Fabric - Navy 150mm

```
Name: Knit Fabric - Navy 150mm
Internal Reference: KF-NAV-150
Category: Knits
Can be Sold: No
Can be Purchased: Yes
Attributes: None
Unit of Measure: Meters
Supplier: [To be confirmed]

Note: Create separate product for each color/width combo.
Do NOT use variants for fabrics - keeps it simple.
```

### Example 3: Product with Special Size (Trousers)

**Product:** Trousers Slim Fit

```
Name: Trousers Slim Fit
Category: Trousers
Can be Sold: Yes
Can be Purchased: Yes
Attributes to Assign: Color, Waist
Attributes: {Color: [White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo],
             Waist: [28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}

Result: 9 colors × 12 waists = 108 variants created automatically
Example variant: Trousers Slim Fit - Navy-34
```

---

## SUPPORT & TROUBLESHOOTING

### Common Issues

**Issue:** Variants not appearing in sales order
- **Solution:** Ensure "Can be Sold" is checked on parent product. Refresh page.

**Issue:** Too many variants to scroll through
- **Solution:** Install Product Matrix module for grid-based selection

**Issue:** Fabric color not available in production BOM
- **Solution:** Check that fabric product exists and is "Can be Purchased" = Yes

**Issue:** BOM consumption doesn't match actual usage
- **Solution:** Validate with CMT in January 2026. Update BOM accordingly.

### Key Contacts

- **Odoo Technical:** [Admin Name/Contact]
- **Product Manager:** [Name/Contact]
- **CMT Partner:** [Contact Info - for BOM validation]
- **Finance/Costing:** [Name/Contact]

---

## APPENDIX: HELPFUL ODOO PATHS

| Task | Path |
|------|------|
| Create Product Attributes | Inventory > Products > Attributes |
| Create Product Categories | Inventory > Products > Categories |
| Create Products | Inventory > Products > Products |
| Create BOMs | Manufacturing > Master Data > Bills of Material |
| View Product Variants | Inventory > Products > Products > [Select Product] > Variants Tab |
| Create Sales Order | Sales > Orders > Quotations |
| View Product Matrix (if enabled) | Sales > Orders > Quotations > [Product Line] > [Matrix Icon] |

---

**Document Prepared:** December 19, 2025
**Status:** Ready for Implementation
**Next Review:** Post Go-Live (Week 1)
