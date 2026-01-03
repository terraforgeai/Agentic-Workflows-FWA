# FAITH WEAR APPAREL (FWA) - PRODUCT CATEGORY HIERARCHY
## Complete Structure for Odoo Implementation - Go-Live Monday

---

## ROOT CATEGORIES OVERVIEW

```
├── GOODS (Finished Goods - Locally Sourced/Manufactured)
├── IMPORTED GOODS (Finished Goods - Imported)
├── RAW MATERIAL (Raw Materials - Locally Sourced)
├── RAW MATERIAL IMPORTS (Raw Materials - Imported)
└── SERVICES (Manufacturing & Value-Add Services)
```

---

## 1. GOODS - Finished Goods (Locally Manufactured/Purchased)

### 1.1 ACCESSORIES
├── **Caps**
│   ├── Caps Regular (Local ZW) - *Supplier TBD*
│   └── *Note: Imported Trucker variants in IMPORTED GOODS / CAPS*
│
└── **Bags**
    ├── Travel Bag - *Supplier TBD*
    └── GYM Bag - *Supplier TBD*

### 1.2 BOTTOMS
├── **Trousers**
│   └── Trousers Slim Fit (Paramount Garments Works, ZW)
│       - Waist Sizes: 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50
│       - Color Variants: White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo
│
└── **Tracksuit**
    ├── Tracksuit Bottom Men - *Supplier TBD*
    │   - Men's Sizes: S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL
    │   - Color Variants: TBD
    │
    └── Tracksuit Bottom Ladies - *Supplier TBD*
        - Ladies Sizes: XS, S, M, L, XL, XXL
        - Color Variants: TBD

### 1.3 OUTERWEAR
└── **Hoodies**
    ├── Hoodie Long Sleeve (Brushed Knitwear) - *Supplier TBD*
    │   - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL)
    │   - Color Variants: TBD
    │
    └── Hoodie Sleeveless (Brushed Knitwear) - *Supplier TBD*
        - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL)
        - Color Variants: TBD
    
    *(Long Hoodie variant below knees - ON HOLD pending classification)*

### 1.4 TOPS
├── **Golf Shirts**
│   └── Golf Shirt Regular Men (Local CMT Manufacturing)
│       - Knit Fabric: 150mm width (flexible composition, color, weight)
│       - Sizes: S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL
│       - Color Variants: White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo (9 total)
│       - Total Variants: 9 colors x 8 sizes = 72 SKUs
│       - **BOM Required:** Knit Fabric (150mm), FWA Labels, Buttons (CMT-supplied), Thread (CMT-supplied)
│       - **Note:** Each fabric width change = new product record + new BOM
│
├── **T-Shirts**
│   └── T-Shirt Regular Round Neck (Purchased - African Threads, Kutaura Enterprises, ZW)
│       - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL), Kids (3-14 age groups)
│       - Color Variants: White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo (9 total)
│       - Total Variants: Multiple per size category
│
├── **Woven Shirts**
│   ├── Short Sleeve Woven Shirt (Purchased) - *Supplier TBD*
│   │   - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL)
│   │   - Color Variants: TBD
│   │
│   └── Long Sleeve Woven Shirt (Purchased) - *Supplier TBD*
│       - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL)
│       - Color Variants: TBD
│
├── **Kids**
│   └── Kids T-Shirt (Purchased) - *Supplier TBD*
│       - Kids Sizes: 3-4, 5-6, 7-8, 9-10, 11-12, 13-14
│       - Color Variants: TBD
│
├── **Tracksuit**
│   ├── Tracksuit Top Men (Purchased) - *Supplier TBD*
│   │   - Men's Sizes: S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL
│   │   - Color Variants: TBD
│   │   - *Coordinated with Tracksuit Bottom Men*
│   │
│   └── Tracksuit Top Ladies (Purchased) - *Supplier TBD*
│       - Ladies Sizes: XS, S, M, L, XL, XXL
│       - Color Variants: TBD
│       - *Coordinated with Tracksuit Bottom Ladies*
│
└── **Aprons**
    └── Apron Chambre Denim Black (Custom) - *Recent Client Order*
        - Color: Black only (may expand)
        - Size Variants: TBD
        - Note: Potential to expand to other colors/styles

---

## 2. IMPORTED GOODS - Imported Finished Goods

### 2.1 GOLF SHIRTS
└── **Golf Shirt Fancy** (RT Knits, Mauritius)
    - Premium/Fancy variant imported as finished goods
    - Sizes: Men's (S-XXXXXL), Ladies (XS-XXL)
    - Color Variants: TBD
    - Note: Different from Local CMT Golf Shirts

### 2.2 CAPS
├── **Caps Trucker Regular** (ex South Africa, Made in China)
│   - Color Variants: TBD
│   - Imported variant
│
└── **Caps Trucker Fancy** (ex South Africa, Made in China)
    - Color Variants: TBD
    - Premium imported variant

---

## 3. RAW MATERIAL - Locally Sourced Materials

### 3.1 FABRICS
└── **Knits**
    ├── Knit Fabric - Navy 150mm
    ├── Knit Fabric - Black 150mm
    ├── Knit Fabric - White 150mm
    ├── Knit Fabric - Red 150mm
    ├── Knit Fabric - Orange 150mm
    ├── Knit Fabric - Blue 150mm
    ├── Knit Fabric - Green 150mm
    ├── Knit Fabric - Putty 150mm
    └── Knit Fabric - Mayo 150mm
    
    **Note:** Each Color + Width = Separate Product
    - Consumption Unit: Metres
    - Standard Width: 150mm (when width changes, new product + new BOM required)
    - Structure: Each fabric is independent product - NO COLOR VARIANTS
    - **Used in:** Golf Shirt Regular Men BOM (CMT Manufacturing)

### 3.2 TRIMS
└── **Labels**
    └── FWA Label (Local Supplier TBD)
        - Unit: Piece
        - Used in: Golf Shirt Regular Men BOM

---

## 4. RAW MATERIAL IMPORTS - Imported Raw Materials

### 4.1 FABRICS
└── **Imported Fabrics** (TBD)
    - For potential imported knit/woven fabrics
    - Structure: Similar to Raw Material / Fabrics

### 4.2 TRIMS
└── **Imported Trims** (TBD)
    - Buttons, thread, labels sourced internationally
    - To be populated as needed

---

## 5. SERVICES - Manufacturing & Value-Add Services

### 5.1 CMT
└── Cut, Make, Trim Services
    - Provided by local CMT partner
    - Used for: Golf Shirt Regular Men production

### 5.2 EMBROIDERY
└── Embroidery Services
    - Value-add service offering

### 5.3 PRINTING
└── Printing Services
    - Value-add service offering

---

## PRODUCT ATTRIBUTES & VARIANTS

### Colors (9 Standard)
White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo

### Sizes - Men's (8 sizes)
S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL

### Sizes - Ladies (6 sizes)
XS, S, M, L, XL, XXL

### Sizes - Kids (Age Groups)
3-4, 5-6, 7-8, 9-10, 11-12, 13-14

### Sizes - Trousers (Waist, 12 sizes)
28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50

---

## KEY IMPLEMENTATION NOTES

### 1. FINISHED PRODUCTS - VARIANT STRATEGY
- **One product record per style** (e.g., "Golf Shirt Regular Men")
- **Color + Size variants** within that product
- **Exception:** Different fabric width or significant yarn/weight change = new product record + new BOM

### 2. RAW MATERIALS - FABRIC STRUCTURE
- **Each fabric = separate product** (no color variants)
- **Naming Convention:** [Fabric Type] - [Color] - [Width]
- Example: "Knit Fabric - Navy 150mm"
- **Why?** Keeps BOMs clean and simple for staff training

### 3. BOM FLEXIBILITY
- **Golf Shirt Regular Men BOM** uses generic "Knit Fabric 150mm" component
- Staff can substitute specific fabric color as long as width remains 150mm
- **January 2026:** Collaborate with CMT to confirm consumption rates and refine BOMs

### 4. SALES ORDER CAPTURE
- **Critical:** Every sales order MUST record: Product, Color, Size, Quantity
- Print layouts should emphasize these fields for easy reference

### 5. SUPPLIERS - TBD (TO BE DETERMINED)
The following require supplier confirmation before Monday Go-Live:
- Kids T-Shirts
- Woven Shirts (Short & Long Sleeve)
- Hoodies (Brushed Knitwear)
- Tracksuits (Tops & Bottoms)
- Bags (Travel Bag, GYM Bag)
- Caps (Local Regular variant)
- Aprons (expansion beyond Chambre Denim Black)
- Raw Materials: Knit Fabrics, FWA Labels

---

## NEXT STEPS - GO-LIVE PREPARATION

### By Friday Evening:
- [ ] Load all Product Categories into Odoo
- [ ] Setup Product Attributes (Color, Size, Waist)
- [ ] Confirm missing supplier details

### By Saturday:
- [ ] Create all Finished Goods products with variants
- [ ] Create Raw Material products (Fabrics, Trims)
- [ ] Setup print layouts for sales orders

### By Sunday:
- [ ] Create BOMs for CMT products (Golf Shirt Regular Men)
- [ ] Validate all products, variants, and BOMs
- [ ] Final data integrity check

### Monday Go-Live:
- [ ] Conduct staff training on product management
- [ ] Test sales order workflows (Color + Size capture)
- [ ] Monitor first day operations

### January 2026:
- [ ] Collaborate with CMT on fabric consumption validation
- [ ] Refine and finalize BOMs
- [ ] Update supplier details as confirmed
- [ ] Expand product line as needed (Aprons, etc.)

---

## SUMMARY

**Total Product Categories:** 30 categories (root + subcategories)

**Finished Goods Products (Estimated):** 20+ products (with multiple variants each)

**Raw Material Products (Estimated):** 15+ SKUs (fabrics by color/width, trims)

**Service Categories:** 3 (CMT, Embroidery, Printing)

**Critical Workflows:**
1. Fabric selection and BOM flexibility for CMT manufacturing
2. Color + Size variant capture in sales orders
3. Supplier management (15+ TBD items to confirm)
4. Inventory tracking by color and size

---

**Prepared for:** Faith Wear Apparel Live Implementation - Monday Go-Live
**Document Date:** December 19, 2025
**Status:** Ready for Odoo Implementation
