# Vendors and Suppliers Directive

## Purpose
Define all vendors, suppliers, and service providers for Faith Wear Apparel operations.

---

## CMT (Cut, Make, Trim) Partners

### Sandy CMT - Zimbabwe (Primary CMT)
| Field | Value |
|-------|-------|
| Vendor Name | Sandy CMT |
| Location | Zimbabwe |
| Service Type | CMT Manufacturing |
| Products | Golf Shirt Regular Men |
| Lead Time | 7-14 days production |
| Notes | Primary CMT partner for locally manufactured golf shirts |

**Odoo Setup:**
- Create as Vendor (res.partner with supplier_rank > 0)
- CMT Service set up as **Storable Product** (not Service) for BOM compatibility
- Product Name: `CMT Service - Sandy Zimbabwe`

---

## Finished Goods Suppliers

### RT Knits - Mauritius
| Field | Value |
|-------|-------|
| Vendor Name | RT Knits |
| Location | Mauritius |
| Type | Finished Goods Importer |
| Products | Golf Shirt Fancy (imported) |
| Lead Time | TBD |

**Products from RT Knits:**
- Golf Shirt Fancy Men (6 colors × 8 sizes = 48 variants)
- Golf Shirt Fancy Ladies (if applicable)

---

### Paramount Garments Works - Zimbabwe
| Field | Value |
|-------|-------|
| Vendor Name | Paramount Garments Works |
| Location | Zimbabwe |
| Type | Finished Goods Supplier |
| Products | Trousers Slim Fit |

**Products:**
- Trousers Slim Fit (9 colors × 12 waist sizes = 108 variants)
- Waist sizes: 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50
- Colors: White, Black, Red, Orange, Navy, Blue, Green, Putty, Mayo

---

### African Threads / Kutaura Enterprises - Zimbabwe
| Field | Value |
|-------|-------|
| Vendor Name | African Threads / Kutaura Enterprises |
| Location | Zimbabwe |
| Type | Finished Goods Supplier |
| Products | T-Shirts |

**Products:**
- T-Shirt Regular Round Neck (Men's, Ladies, Kids)

---

## Value-Add Service Providers

### Embroidery Dave
| Field | Value |
|-------|-------|
| Vendor Name | Embroidery Dave |
| Location | Zimbabwe |
| Service Type | Logo/Branding Embroidery |
| Used For | Corporate branding on apparel |

**Odoo Setup:**
- Create as Vendor
- Can be added to BOM as service component if tracking required

---

## Raw Material Suppliers

### Fabric Suppliers (TBD)
| Material | Supplier | Notes |
|----------|----------|-------|
| La Coste Knit - Navy 150mm | TBD | Primary golf shirt fabric |
| La Coste Knit - Black 150mm | TBD | |
| La Coste Knit - White 150mm | TBD | |
| La Coste Knit - Red 150mm | TBD | |
| La Coste Knit - Orange 150mm | TBD | |
| La Coste Knit - Blue 150mm | TBD | |
| La Coste Knit - Green 150mm | TBD | |
| La Coste Knit - Putty 150mm | TBD | |
| La Coste Knit - Mayo 150mm | TBD | |

### Label Supplier
| Field | Value |
|-------|-------|
| Vendor Name | Label Supplier MU |
| Location | Mauritius |
| Products | FWA Woven Labels |

---

## Imported Goods Suppliers

### Caps - South Africa (Made in China)
| Field | Value |
|-------|-------|
| Source | South Africa (ex China) |
| Products | Caps Trucker Regular, Caps Trucker Fancy |

---

## Vendor Categories Summary

| Category | Vendors |
|----------|---------|
| **CMT Manufacturing** | Sandy CMT (Zimbabwe) |
| **Embroidery** | Embroidery Dave |
| **Finished Goods - Import** | RT Knits (Mauritius) |
| **Finished Goods - Local** | Paramount Garments, African Threads, Kutaura |
| **Raw Materials - Fabric** | TBD |
| **Raw Materials - Labels** | Label Supplier MU |
| **Accessories - Caps** | SA/China supplier |

---

## Vendor Setup in Odoo

### Required Fields
```
Name: [Vendor Name]
Is Company: Yes
Type: Contact
Supplier Rank: 1 (or higher)
Customer Rank: 0 (unless also a customer)
Country: [Country]
Phone: [Contact Number]
Email: [Email]
Payment Terms: [As negotiated]
```

### Vendor Pricelist (Optional)
For each vendor, can set up:
- Product-specific pricing
- Minimum order quantities
- Lead times

---

## Key Contacts

| Role | Name | Vendor |
|------|------|--------|
| CMT Contact | Sandy | Sandy CMT |
| Embroidery Contact | Dave | Embroidery Dave |

---

## Last Updated
3 January 2026 - Compiled from FWA business analysis data
