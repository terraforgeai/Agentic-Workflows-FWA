# FWA ODOO GO-LIVE - QUICK REFERENCE CARD
## Staff Guide - Print & Post at Your Desk

---

## FAST FACTS

| What | Details |
|------|---------|
| **Go-Live Date** | Monday, December 23, 2025 |
| **System** | Odoo ERP |
| **New Process** | All sales orders MUST include: Product + Color + Size + Quantity |
| **Product Lines** | Apparel (Golf Shirts, T-Shirts, Trousers, Caps, etc.) |

---

## THE 5 THINGS YOU NEED TO KNOW

### 1️⃣ PRODUCTS NOW HAVE COLOR + SIZE VARIANTS
- Old system: One "Golf Shirt" product
- **New system:** "Golf Shirt Regular Men" with 72 variants (9 colors × 8 sizes)
- You don't create variants—Odoo creates them automatically

### 2️⃣ FABRIC IS DIFFERENT FROM FINISHED GOODS
- **Fabrics (Raw Materials):** Each color = separate product
  - Example: "Knit Fabric - Navy 150mm" (NOT a variant)
  - Example: "Knit Fabric - Black 150mm" (NOT a variant)
  - Why? Keeps BOMs simple for production

- **Finished Goods:** Uses Color + Size variants
  - Example: "Golf Shirt Regular Men" with Navy-L, White-M, etc.

### 3️⃣ SALES ORDER ENTRY IS FASTER (Once You Learn It)
- Select: **Product** → **Color** → **Size** → **Quantity**
- Options:
  - **Option A** (Variant List): Click "Golf Shirt Regular Men - Navy-L"
  - **Option B** (Matrix Grid): Click Navy, then click L (faster!)

### 4️⃣ FABRIC WIDTH MATTERS
- Standard fabric width: **150mm**
- If width changes → Need new BOM
- Example: "Golf Shirt Regular Men - 160mm width" = new product + new BOM

### 5️⃣ CMT & SUPPLIERS
- **Golf Shirt Regular Men:** Made locally by CMT partner
- **T-Shirts, Trousers, Caps, etc.:** Purchased from suppliers
- **Important:** Color and size MUST be captured in every sales order

---

## SALES TEAM - HOW TO ENTER A SALES ORDER

### Step-by-Step

1. **Click:** Sales > Quotations > Create
2. **Fill:** Customer name, delivery date
3. **Click:** Add Line
4. **Select:** Product (e.g., "Golf Shirt Regular Men")
5. **Select:** Color (e.g., Navy)
6. **Select:** Size (e.g., L)
7. **Enter:** Quantity (e.g., 100)
8. **System Fills:** Price, Total
9. **Repeat** for other products/colors/sizes
10. **Save & Send** to customer

### Example Sales Order
```
LINE 1: Golf Shirt Regular Men | Navy | L | 50 pcs
LINE 2: Golf Shirt Regular Men | White | M | 75 pcs
LINE 3: T-Shirt Regular | Black | S | 100 pcs
LINE 4: Trousers Slim Fit | Navy | Waist 34 | 50 pcs

TOTAL: $4,500
```

**Key:** Each line shows Color & Size clearly!

---

## WAREHOUSE TEAM - PICKING & PACKING

### Stock Keeping by Color & Size

- **Old System:** "Golf Shirt" bin
- **New System:** Separate bins or labels for:
  - Golf Shirt Regular Men - Navy
  - Golf Shirt Regular Men - White
  - Golf Shirt Regular Men - Black
  - etc.

### Picking a Sales Order
1. Receive picking list from Odoo
2. List shows: **Product | Color | Size | Quantity needed**
3. Example:
   ```
   Product           | Color | Size | Qty
   Golf Shirt Reg    | Navy  | L    | 50
   Golf Shirt Reg    | White | M    | 75
   T-Shirt Regular   | Black | S    | 100
   ```
4. Pick items by color + size
5. Scan & confirm in Odoo
6. Move to packing

**Tip:** Request picking list in a color-coded format for faster picking!

---

## PRODUCTION (CMT) TEAM

### Golf Shirt Regular Men - What's New?

**BOM (Bill of Materials):**
```
1 piece Golf Shirt Regular Men requires:
- Knit Fabric 150mm: [amount] meters
- FWA Label: 1 piece
- Buttons: [provided by CMT]
- Thread: [provided by CMT]
```

**Fabric Selection:**
- Any knit fabric that is 150mm wide works
- Can switch from Navy to Black (no BOM change)
- If width changes to 160mm → Need different BOM

**January 2026:** We'll confirm exact consumption with CMT partner

### Production Planning
- Every sales order specifies: Color, Size, Quantity
- Production can see exactly what's needed
- Use Odoo picking list for fabric allocation

---

## FINANCE/COSTING TEAM

### Costing Updates

**Golf Shirt Regular Men:**
- Cost = BOM cost (fabric + labor)
- Different fabrics = different cost (track separately if needed)
- Margin = Selling Price - Cost

**Pricing Strategy:**
- All colors same price? (Likely yes)
- All sizes same price? (Likely yes, but set in Odoo)

**Reporting:**
- Reports now show: Product | Color | Size | Qty Sold | Revenue
- Example: "Golf Shirt Regular Men - Navy-L sold 250 units - $2,125"

---

## COMMON QUESTIONS & ANSWERS

### Q: What if a customer orders "Golf Shirt in Navy"—what size?
**A:** Ask! Odoo requires Color AND Size. Your job is to confirm both with customer.

### Q: Can I use just "Golf Shirt" without specifying color/size?
**A:** No. Odoo won't let you. You MUST select color and size to create a sales order.

### Q: What if we run out of Navy-L but have Navy-XL?
**A:** Can't substitute. Customer ordered Navy-L specifically. Contact them for options.

### Q: How do I know all the colors/sizes available?
**A:** When you select a product, Odoo shows you the variant list (or matrix grid). Pick from there.

### Q: What if a new color/size combination is needed?
**A:** Product Manager adds it. Odoo auto-creates the variant. Check back in a few hours.

### Q: Why can't fabrics be "Knit Fabric - Multiple Colors"?
**A:** Because each color is a separate item in the warehouse. Odoo needs to track Navy separately from Black separately from White separately. This is for inventory accuracy.

### Q: When will BOMs be finalized?
**A:** January 2026, after we work with CMT partner. For now, they're estimates.

---

## KEYBOARD SHORTCUTS & TIPS

| Shortcut | Action |
|----------|--------|
| `Alt+C` | Create new record (in many screens) |
| `Ctrl+S` | Save |
| `Ctrl+Z` | Undo |
| Tab | Move to next field |
| Click product field | Opens dropdown with all variants |

**Pro Tip:** If selecting variants is slow, ask your manager for "Product Matrix" module (faster grid-based selection)

---

## WHEN SOMETHING GOES WRONG

### Issue: Can't find a color/size variant
**Action:** 
1. Check product name spelling
2. Check color spelling (is it "Navy" or "Navy Blue"?)
3. Refresh page
4. Contact Product Manager

### Issue: Got an error message when saving sales order
**Action:**
1. Read error message carefully
2. Common: Missing field (Color, Size, Quantity)
3. Fill in all required fields (marked with *)
4. Save again
5. If still stuck → Escalate to Odoo Admin

### Issue: Price looks wrong
**Action:**
1. Check that you selected the right variant (color matters!)
2. Confirm size is correct (shouldn't affect price, but double-check)
3. Take screenshot of issue
4. Report to Finance Manager

### Escalation Contact
- **Immediate Help:** [Local Supervisor Name]
- **Odoo Technical:** [Odoo Admin Name] - [Phone/Email]
- **Product Questions:** [Product Manager Name] - [Phone/Email]

---

## FIRST WEEK MINDSET

✅ **DO:**
- Ask questions if unsure
- Take detailed notes on what confused you
- Double-check color/size before submitting orders
- Give feedback on what's working/not working
- Be patient—everyone is learning

❌ **DON'T:**
- Bypass the system to "get it done faster"
- Ignore error messages (they're trying to help!)
- Skip color/size selection (even if you "know" what they ordered)
- Assume the old way still works (it doesn't!)
- Keep quiet about problems

---

## DAILY CHECKLIST

### Start of Day
- [ ] Odoo is open and I can log in
- [ ] Dashboard shows my tasks
- [ ] I can see the product list with colors/sizes

### During Work
- [ ] Every sales order includes: Product + Color + Size + Qty
- [ ] No shortcuts on variant selection
- [ ] Questions captured for training session

### End of Day
- [ ] Sales orders saved
- [ ] Picking lists generated correctly
- [ ] Any issues reported to supervisor

---

## HELPFUL RESOURCES

| Resource | Location |
|----------|----------|
| Product List with Colors/Sizes | Inventory > Products |
| How to Create Sales Order | Documentation folder on desktop |
| BOM Details (Production) | Manufacturing > Bills of Material |
| FAQs | Posted in break room |
| Video Tutorials | [Link from Odoo Admin] |

---

## REMEMBER

**Old Way:** Enter a vague order → Hope production understands → Mistakes happen

**New Way:** Sales order specifies Color + Size exactly → Production knows precisely what to make → Fewer mistakes, faster delivery

**Your Role:** You're the keeper of accuracy. Take 10 extra seconds to confirm color and size. It saves hours of problems downstream.

---

## ONE MORE THING

**This is new for everyone.** Including management. Everyone will make mistakes. That's normal. The key is:
1. Notice the mistake quickly
2. Fix it
3. Learn from it
4. Help the team learn from it

**We're in this together.** Welcome to the new FWA system! 🎉

---

**Questions?** Post on the team channel or ask your supervisor.

**Feedback?** Use the feedback form [link from admin].

**Good luck!** You've got this. 💪

---

*Distributed: December 20, 2025*
*Updated: As needed during first week*
