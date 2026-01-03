# Product Structure Directive

## Purpose
Define the standard product structure and naming conventions for FWA in Odoo. This ensures BOMs work consistently and inventory tracking is accurate.

## Key Principle: Variants at Finished Goods Level Only

**Fabrics and raw materials are created as INDIVIDUAL PRODUCTS (including colorway), NOT as variants.**

**Finished goods use VARIANTS for size/color combinations.**

This approach was determined through testing to ensure BOMs work consistently.

---

## Product Structure

### Layer 1: Raw Materials (No Variants)

Each fabric/material is a separate product record, including the colorway:

| Product Name | SKU | Type | Category |
|--------------|-----|------|----------|
| Cotton Pique - Navy | FAB-CP-NAVY | Storable | Raw Materials / Fabric |
| Cotton Pique - White | FAB-CP-WHITE | Storable | Raw Materials / Fabric |
| Cotton Pique - Black | FAB-CP-BLACK | Storable | Raw Materials / Fabric |
| Polyester Mesh - Red | FAB-PM-RED | Storable | Raw Materials / Fabric |
| Polyester Mesh - Blue | FAB-PM-BLUE | Storable | Raw Materials / Fabric |

**Why individual products for fabrics?**
- BOMs reference specific fabric products directly
- No variant complexity in component selection
- Clearer inventory tracking per colorway
- Simpler purchasing (order specific fabric colors)
- Avoids BOM variant matching issues

### Layer 2: Components (No Variants)

Components are also individual products:

| Product Name | SKU | Type | Category |
|--------------|-----|------|----------|
| Thread - Navy | THR-NAVY | Storable | Raw Materials / Thread |
| Thread - White | THR-WHITE | Storable | Raw Materials / Thread |
| Label - FWA Woven | LBL-FWA-W | Storable | Raw Materials / Labels |
| Label - Care Instructions | LBL-CARE | Storable | Raw Materials / Labels |
| Button - White 4-hole | BTN-W-4H | Storable | Raw Materials / Buttons |
| Polybag - Medium | PKG-POLY-M | Storable | Packaging |

### Layer 3: Finished Goods (WITH Variants)

Finished goods use product templates with variants for **Size** (and optionally **Color** if the same BOM applies):

**Product Template:** Golf Shirt Regular

| Variant | SKU | Attributes |
|---------|-----|------------|
| Golf Shirt Regular - S | GSR-S | Size: S |
| Golf Shirt Regular - M | GSR-M | Size: M |
| Golf Shirt Regular - L | GSR-L | Size: L |
| Golf Shirt Regular - XL | GSR-XL | Size: XL |
| Golf Shirt Regular - 2XL | GSR-2XL | Size: 2XL |

**Note:** If different colors require different fabric BOMs, create separate product templates:
- Golf Shirt Regular Navy (variants: S, M, L, XL, 2XL)
- Golf Shirt Regular White (variants: S, M, L, XL, 2XL)

---

## BOM Structure

### Example: Golf Shirt Regular Navy - Size M

**Product:** Golf Shirt Regular Navy - M (GSR-NAVY-M)

**Manufacturing:** CMT Subcontracted (Zimbabwe)

**Bill of Materials (Subcontracting BOM):**

| Component | Quantity | UoM | Notes |
|-----------|----------|-----|-------|
| Cotton Pique - Navy | 1.5 | m | Fabric (specific colorway) |
| Thread - Navy | 1 | Unit | Matching thread |
| Label - FWA Woven | 1 | Unit | Brand label |
| Label - Care Instructions | 1 | Unit | Care label |
| Button - White 4-hole | 3 | Unit | Collar buttons |
| Polybag - Medium | 1 | Unit | Packaging |

**Key Point:** The BOM references `Cotton Pique - Navy` directly, not a variant of a generic "Cotton Pique" product.

---

## CMT Manufacturing Model (Zimbabwe)

FWA uses a **CMT (Cut, Make, Trim) model** for golf shirt production with **Sandy CMT** in Zimbabwe.

### CRITICAL: Use Manufacturing, NOT Subcontracting

> **250+ hours of testing (Nov-Dec 2025) confirmed:**
> - Use **Manufacturing** route, NOT Odoo's Subcontracting module
> - CMT service must be set up as a **physical product** (not a service) for BOM to work
> - This enables proper SO → MO automation

### CMT Service Product Setup

**Sandy CMT** is set up as a product in Odoo:

| Field | Value |
|-------|-------|
| Product Name | CMT Service - Sandy Zimbabwe |
| Product Type | **Storable Product** (NOT Service) |
| Category | FWA / Services |
| Notes | Physical product type required for BOM functionality |

### Flow
```
1. FWA purchases raw materials (fabric, thread, labels, buttons)
2. Sales Order created → Manufacturing Order auto-generated
3. MO consumes components + CMT service
4. Finished goods produced and added to stock
```

### BOM Structure (with CMT as component)

| Component | Quantity | UoM | Notes |
|-----------|----------|-----|-------|
| Cotton Pique - Navy | 1.5 | m | Fabric |
| Thread - Navy | 1 | Unit | Thread |
| Label - FWA Woven | 1 | Unit | Brand label |
| CMT Service - Sandy Zimbabwe | 1 | Unit | **CMT as physical product** |
| *(other components)* | | | |

### Why Manufacturing over Subcontracting?

After extensive testing:
1. **SO → MO automation works** - Sales Orders correctly trigger Manufacturing Orders
2. **BOM consistency** - CMT as physical product integrates into BOM properly
3. **Simpler workflow** - Avoids subcontracting module complexity
4. **Odoo preference** - The system handles this route more reliably

### Lead Times (Zimbabwe CMT)
- Component shipping to Zimbabwe: 3-5 days
- CMT production: 7-14 days (depending on volume)
- Return shipping: 3-5 days
- **Total lead time: 2-4 weeks**

---

## Imported Finished Goods Model (Mauritius)

Some finished goods are **imported ready-made** (not manufactured via CMT):

### Example: Golf Shirt Fancy

**Supplier:** RT Knits (Mauritius)

**Product Type:** Purchased Finished Good (no BOM required)

**Flow:**
```
1. FWA creates Purchase Order to RT Knits
2. Finished goods shipped from Mauritius
3. Received into WHFWA/Stock
```

**Key Differences from CMT:**
- No BOM needed - product is purchased complete
- No component tracking - supplier manages materials
- Simple PO → Receipt workflow
- Product marked as `purchase_ok = True`, no manufacturing route

### Products from RT Knits (Mauritius)
- Golf Shirt Fancy (variants: sizes)
- *(add others as identified)*

---

## Naming Conventions

### Raw Materials
```
[Material Type] - [Color/Specification]
```
Examples:
- Cotton Pique - Navy
- Polyester Mesh - Royal Blue
- Ribbing - White

### Components
```
[Component Type] - [Specification]
```
Examples:
- Thread - Navy
- Button - White 4-hole
- Zipper - Black 20cm

### Finished Goods (Template)
```
[Product Type] [Style] [Color]
```
Examples:
- Golf Shirt Regular Navy
- Golf Shirt Slim White
- Polo Shirt Classic Black
- Cap Structured Navy

### Finished Goods (Variant)
```
[Product Type] [Style] [Color] - [Size]
```
Examples:
- Golf Shirt Regular Navy - M
- Golf Shirt Regular Navy - L
- Polo Shirt Classic Black - XL

---

## SKU Conventions

### Raw Materials
```
[TYPE]-[MATERIAL]-[COLOR]
```
- `FAB-CP-NAVY` = Fabric, Cotton Pique, Navy
- `FAB-PM-RED` = Fabric, Polyester Mesh, Red
- `THR-NAVY` = Thread, Navy

### Finished Goods
```
[PRODUCT][STYLE]-[COLOR]-[SIZE]
```
- `GSR-NAVY-M` = Golf Shirt Regular, Navy, Medium
- `GSS-WHITE-L` = Golf Shirt Slim, White, Large
- `CAP-STR-BLK` = Cap Structured, Black

---

## Product Categories

```
FWA
├── Finished Goods
│   ├── Golf Shirts
│   ├── Polo Shirts
│   ├── T-Shirts
│   └── Caps
├── Raw Materials
│   ├── Fabric
│   ├── Thread
│   ├── Labels
│   ├── Buttons
│   └── Zippers
├── Components
│   └── Trims
└── Packaging
    ├── Polybags
    └── Boxes
```

---

## Odoo Configuration Notes

### Product Attributes (for Finished Goods only)
- **Size:** S, M, L, XL, 2XL, 3XL
- **Color:** (Optional - only if same BOM applies to all colors)

### Units of Measure
- Fabric: **m** (meters)
- Thread: **Unit** or **Spool**
- Labels, Buttons, Components: **Unit**
- Finished Goods: **Unit**

### Product Type
- All physical items: **Storable Product**
- Services (e.g., CMT subcontracting): **Service**

---

## Why This Structure Works

1. **BOM Consistency:** Components are fixed references, no variant matching needed
2. **Clear Inventory:** Know exactly how much "Cotton Pique - Navy" you have
3. **Simple Purchasing:** Order specific fabric colors from suppliers
4. **Variant Flexibility:** Sizes handled at finished goods level where it matters
5. **Reporting:** Easy to report on fabric usage by colorway

---

## Related Scripts
- `execution/bulk_import_products.py` - Use for importing product catalog

## Last Updated
2 January 2026 - Initial directive based on BOM testing findings
