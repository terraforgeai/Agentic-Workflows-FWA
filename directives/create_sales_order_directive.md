# Create Sales Order Directive

## Purpose
Create a new Sales Order in Odoo for customer orders, typically for golf shirts, branded apparel, or other FWA products. This triggers the sales-to-manufacturing workflow.

## Inputs
| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| customer_name | string | Yes | "ACME Corporation" |
| customer_id | integer | No | 42 (if known, faster lookup) |
| products | list | Yes | See product structure below |
| delivery_date | date | No | "2026-01-15" |
| customer_ref | string | No | "PO-12345" (customer's PO number) |
| notes | string | No | "Urgent order - priority shipping" |

### Product Structure
```json
{
  "product_name": "Golf Shirt - Blue - Size M",
  "product_id": 123,  // Optional if name provided
  "quantity": 500,
  "unit_price": 45.00,  // Optional - uses default if not provided
  "discount": 0  // Optional percentage
}
```

## Prerequisites
- [ ] Odoo connection active (`python execution/odoo_connect.py --test`)
- [ ] Customer exists in Odoo (res.partner with customer_rank > 0)
- [ ] Products exist in Odoo with valid BOMs (if manufacturing required)
- [ ] User has Sales / User permissions

## Steps
1. **Validate inputs**
   - Customer name or ID provided
   - At least one product line
   - Quantities are positive numbers

2. **Lookup customer**
   - Search res.partner by name or ID
   - Verify customer_rank > 0
   - Get invoice/shipping addresses

3. **Lookup products**
   - Search product.product by name or ID
   - Verify products are active and sale_ok = True
   - Get default prices from pricelist

4. **Create Sales Order**
   - Create sale.order header
   - Create sale.order.line for each product
   - Order created in 'draft' state

5. **Optional: Confirm order**
   - If auto_confirm = True, call action_confirm()
   - This triggers manufacturing orders if MTO

6. **Return result**
   - Sales Order ID and reference number
   - Order line details
   - Any warnings (low stock, etc.)

## Outputs

### Success
```json
{
  "status": "success",
  "order_id": 456,
  "order_ref": "S00123",
  "customer": "ACME Corporation",
  "total_amount": 22500.00,
  "order_lines": [
    {"product": "Golf Shirt - Blue - Size M", "qty": 500, "subtotal": 22500.00}
  ],
  "state": "draft",
  "message": "Sales Order S00123 created successfully"
}
```

### Failure
```json
{
  "status": "error",
  "error_type": "not_found",
  "message": "Customer 'ACME Corp' not found in Odoo",
  "suggestions": ["Check spelling", "Use customer_id if known", "Create customer first"]
}
```

## Edge Cases

### Customer not found
- Search with fuzzy matching (name ilike '%ACME%')
- Return list of similar customers for user to choose
- Option to create new customer

### Product not found
- Search with fuzzy matching
- Check if product is archived (active = False)
- Return similar products

### Insufficient stock
- Order still created (draft state)
- Warning returned about stock levels
- Manufacturing order will be created on confirmation

### Customer has multiple addresses
- Use main address for both invoice/shipping
- Option to specify different addresses

## Odoo Modules Involved
- **Sales** (sale) - Core order management
- **Inventory** (stock) - Stock checking
- **Manufacturing** (mrp) - MO creation on confirmation (if MTO)

## Related Scripts
- `execution/create_sales_order.py`

## API Notes
- Sales orders created via API are in 'draft' state
- Calling `action_confirm()` confirms and triggers delivery/manufacturing
- Taxes applied based on fiscal position

## Last Updated
2 January 2026 - Initial directive creation
