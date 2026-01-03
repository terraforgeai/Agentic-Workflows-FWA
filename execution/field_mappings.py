#!/usr/bin/env python3
"""
Field Mappings - Odoo Field Definitions for FWA

Purpose: Central reference for Odoo field types, requirements, and mappings
Input: N/A (Reference module)
Output: Field definitions used by execution scripts

This file serves as documentation AND validation reference for all Odoo fields
used in FWA operations.

Related Directive: N/A (Core infrastructure)
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass


class FieldType(Enum):
    """Odoo field types."""
    CHAR = "char"
    TEXT = "text"
    HTML = "html"
    INTEGER = "integer"
    FLOAT = "float"
    MONETARY = "monetary"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    SELECTION = "selection"
    MANY2ONE = "many2one"
    ONE2MANY = "one2many"
    MANY2MANY = "many2many"
    BINARY = "binary"


@dataclass
class FieldDefinition:
    """Definition of an Odoo field."""
    name: str
    field_type: FieldType
    required: bool = False
    readonly: bool = False
    description: str = ""
    relation: Optional[str] = None  # For relational fields
    selection_options: Optional[List[tuple]] = None  # For selection fields
    default: Optional[Any] = None


# =============================================================================
# PARTNER (res.partner) - Customers & Suppliers
# =============================================================================
PARTNER_FIELDS: Dict[str, FieldDefinition] = {
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.CHAR,
        required=True,
        description='Partner name (customer/supplier)'
    ),
    'email': FieldDefinition(
        name='email',
        field_type=FieldType.CHAR,
        description='Email address'
    ),
    'phone': FieldDefinition(
        name='phone',
        field_type=FieldType.CHAR,
        description='Phone number'
    ),
    'mobile': FieldDefinition(
        name='mobile',
        field_type=FieldType.CHAR,
        description='Mobile phone'
    ),
    'street': FieldDefinition(
        name='street',
        field_type=FieldType.CHAR,
        description='Street address line 1'
    ),
    'street2': FieldDefinition(
        name='street2',
        field_type=FieldType.CHAR,
        description='Street address line 2'
    ),
    'city': FieldDefinition(
        name='city',
        field_type=FieldType.CHAR,
        description='City'
    ),
    'zip': FieldDefinition(
        name='zip',
        field_type=FieldType.CHAR,
        description='Postal/ZIP code'
    ),
    'country_id': FieldDefinition(
        name='country_id',
        field_type=FieldType.MANY2ONE,
        relation='res.country',
        description='Country'
    ),
    'state_id': FieldDefinition(
        name='state_id',
        field_type=FieldType.MANY2ONE,
        relation='res.country.state',
        description='State/Province'
    ),
    'is_company': FieldDefinition(
        name='is_company',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Is this a company (vs individual)?'
    ),
    'customer_rank': FieldDefinition(
        name='customer_rank',
        field_type=FieldType.INTEGER,
        default=0,
        description='Customer rank (>0 = is a customer)'
    ),
    'supplier_rank': FieldDefinition(
        name='supplier_rank',
        field_type=FieldType.INTEGER,
        default=0,
        description='Supplier rank (>0 = is a supplier)'
    ),
    'vat': FieldDefinition(
        name='vat',
        field_type=FieldType.CHAR,
        description='Tax ID / VAT number'
    ),
    'ref': FieldDefinition(
        name='ref',
        field_type=FieldType.CHAR,
        description='Internal reference'
    ),
}


# =============================================================================
# PRODUCT (product.product / product.template)
# =============================================================================
PRODUCT_FIELDS: Dict[str, FieldDefinition] = {
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.CHAR,
        required=True,
        description='Product name'
    ),
    'default_code': FieldDefinition(
        name='default_code',
        field_type=FieldType.CHAR,
        description='Internal Reference (SKU)'
    ),
    'barcode': FieldDefinition(
        name='barcode',
        field_type=FieldType.CHAR,
        description='Barcode (EAN13, UPC, etc.)'
    ),
    'type': FieldDefinition(
        name='type',
        field_type=FieldType.SELECTION,
        required=True,
        selection_options=[
            ('consu', 'Consumable'),
            ('service', 'Service'),
            ('product', 'Storable Product'),
        ],
        default='product',
        description='Product type'
    ),
    'categ_id': FieldDefinition(
        name='categ_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='product.category',
        description='Product category'
    ),
    'list_price': FieldDefinition(
        name='list_price',
        field_type=FieldType.FLOAT,
        default=0.0,
        description='Sales price'
    ),
    'standard_price': FieldDefinition(
        name='standard_price',
        field_type=FieldType.FLOAT,
        default=0.0,
        description='Cost price'
    ),
    'uom_id': FieldDefinition(
        name='uom_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='uom.uom',
        description='Unit of Measure'
    ),
    'uom_po_id': FieldDefinition(
        name='uom_po_id',
        field_type=FieldType.MANY2ONE,
        relation='uom.uom',
        description='Purchase Unit of Measure'
    ),
    'tracking': FieldDefinition(
        name='tracking',
        field_type=FieldType.SELECTION,
        selection_options=[
            ('serial', 'By Unique Serial Number'),
            ('lot', 'By Lots'),
            ('none', 'No Tracking'),
        ],
        default='none',
        description='Tracking type'
    ),
    'sale_ok': FieldDefinition(
        name='sale_ok',
        field_type=FieldType.BOOLEAN,
        default=True,
        description='Can be sold'
    ),
    'purchase_ok': FieldDefinition(
        name='purchase_ok',
        field_type=FieldType.BOOLEAN,
        default=True,
        description='Can be purchased'
    ),
    'active': FieldDefinition(
        name='active',
        field_type=FieldType.BOOLEAN,
        default=True,
        description='Active (archived if False)'
    ),
    'description': FieldDefinition(
        name='description',
        field_type=FieldType.TEXT,
        description='Internal notes'
    ),
    'description_sale': FieldDefinition(
        name='description_sale',
        field_type=FieldType.TEXT,
        description='Sales description'
    ),
}


# =============================================================================
# SALES ORDER (sale.order)
# =============================================================================
SALE_ORDER_FIELDS: Dict[str, FieldDefinition] = {
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.CHAR,
        readonly=True,
        description='Order Reference (auto-generated)'
    ),
    'partner_id': FieldDefinition(
        name='partner_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='res.partner',
        description='Customer'
    ),
    'partner_invoice_id': FieldDefinition(
        name='partner_invoice_id',
        field_type=FieldType.MANY2ONE,
        relation='res.partner',
        description='Invoice Address'
    ),
    'partner_shipping_id': FieldDefinition(
        name='partner_shipping_id',
        field_type=FieldType.MANY2ONE,
        relation='res.partner',
        description='Delivery Address'
    ),
    'date_order': FieldDefinition(
        name='date_order',
        field_type=FieldType.DATETIME,
        description='Order Date'
    ),
    'validity_date': FieldDefinition(
        name='validity_date',
        field_type=FieldType.DATE,
        description='Expiration Date'
    ),
    'pricelist_id': FieldDefinition(
        name='pricelist_id',
        field_type=FieldType.MANY2ONE,
        relation='product.pricelist',
        description='Pricelist'
    ),
    'payment_term_id': FieldDefinition(
        name='payment_term_id',
        field_type=FieldType.MANY2ONE,
        relation='account.payment.term',
        description='Payment Terms'
    ),
    'user_id': FieldDefinition(
        name='user_id',
        field_type=FieldType.MANY2ONE,
        relation='res.users',
        description='Salesperson'
    ),
    'team_id': FieldDefinition(
        name='team_id',
        field_type=FieldType.MANY2ONE,
        relation='crm.team',
        description='Sales Team'
    ),
    'client_order_ref': FieldDefinition(
        name='client_order_ref',
        field_type=FieldType.CHAR,
        description='Customer Reference'
    ),
    'note': FieldDefinition(
        name='note',
        field_type=FieldType.TEXT,
        description='Terms and Conditions'
    ),
    'state': FieldDefinition(
        name='state',
        field_type=FieldType.SELECTION,
        readonly=True,
        selection_options=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sales Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        description='Status'
    ),
    'order_line': FieldDefinition(
        name='order_line',
        field_type=FieldType.ONE2MANY,
        relation='sale.order.line',
        description='Order Lines'
    ),
}


# =============================================================================
# SALES ORDER LINE (sale.order.line)
# =============================================================================
SALE_ORDER_LINE_FIELDS: Dict[str, FieldDefinition] = {
    'order_id': FieldDefinition(
        name='order_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='sale.order',
        description='Sales Order'
    ),
    'product_id': FieldDefinition(
        name='product_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='product.product',
        description='Product'
    ),
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.TEXT,
        required=True,
        description='Description'
    ),
    'product_uom_qty': FieldDefinition(
        name='product_uom_qty',
        field_type=FieldType.FLOAT,
        required=True,
        default=1.0,
        description='Quantity'
    ),
    'product_uom': FieldDefinition(
        name='product_uom',
        field_type=FieldType.MANY2ONE,
        relation='uom.uom',
        description='Unit of Measure'
    ),
    'price_unit': FieldDefinition(
        name='price_unit',
        field_type=FieldType.FLOAT,
        description='Unit Price'
    ),
    'discount': FieldDefinition(
        name='discount',
        field_type=FieldType.FLOAT,
        default=0.0,
        description='Discount (%)'
    ),
    'tax_id': FieldDefinition(
        name='tax_id',
        field_type=FieldType.MANY2MANY,
        relation='account.tax',
        description='Taxes'
    ),
}


# =============================================================================
# PURCHASE ORDER (purchase.order)
# =============================================================================
PURCHASE_ORDER_FIELDS: Dict[str, FieldDefinition] = {
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.CHAR,
        readonly=True,
        description='Order Reference (auto-generated)'
    ),
    'partner_id': FieldDefinition(
        name='partner_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='res.partner',
        description='Vendor'
    ),
    'partner_ref': FieldDefinition(
        name='partner_ref',
        field_type=FieldType.CHAR,
        description='Vendor Reference'
    ),
    'date_order': FieldDefinition(
        name='date_order',
        field_type=FieldType.DATETIME,
        description='Order Deadline'
    ),
    'date_planned': FieldDefinition(
        name='date_planned',
        field_type=FieldType.DATETIME,
        description='Expected Arrival'
    ),
    'user_id': FieldDefinition(
        name='user_id',
        field_type=FieldType.MANY2ONE,
        relation='res.users',
        description='Buyer'
    ),
    'currency_id': FieldDefinition(
        name='currency_id',
        field_type=FieldType.MANY2ONE,
        relation='res.currency',
        description='Currency'
    ),
    'notes': FieldDefinition(
        name='notes',
        field_type=FieldType.TEXT,
        description='Terms and Conditions'
    ),
    'state': FieldDefinition(
        name='state',
        field_type=FieldType.SELECTION,
        readonly=True,
        selection_options=[
            ('draft', 'RFQ'),
            ('sent', 'RFQ Sent'),
            ('to approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        description='Status'
    ),
    'order_line': FieldDefinition(
        name='order_line',
        field_type=FieldType.ONE2MANY,
        relation='purchase.order.line',
        description='Order Lines'
    ),
}


# =============================================================================
# MANUFACTURING ORDER (mrp.production)
# =============================================================================
MANUFACTURING_ORDER_FIELDS: Dict[str, FieldDefinition] = {
    'name': FieldDefinition(
        name='name',
        field_type=FieldType.CHAR,
        readonly=True,
        description='Reference (auto-generated)'
    ),
    'product_id': FieldDefinition(
        name='product_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='product.product',
        description='Product to Manufacture'
    ),
    'product_qty': FieldDefinition(
        name='product_qty',
        field_type=FieldType.FLOAT,
        required=True,
        description='Quantity to Produce'
    ),
    'product_uom_id': FieldDefinition(
        name='product_uom_id',
        field_type=FieldType.MANY2ONE,
        relation='uom.uom',
        description='Unit of Measure'
    ),
    'bom_id': FieldDefinition(
        name='bom_id',
        field_type=FieldType.MANY2ONE,
        relation='mrp.bom',
        description='Bill of Materials'
    ),
    'date_planned_start': FieldDefinition(
        name='date_planned_start',
        field_type=FieldType.DATETIME,
        description='Scheduled Start Date'
    ),
    'date_planned_finished': FieldDefinition(
        name='date_planned_finished',
        field_type=FieldType.DATETIME,
        description='Scheduled End Date'
    ),
    'location_src_id': FieldDefinition(
        name='location_src_id',
        field_type=FieldType.MANY2ONE,
        relation='stock.location',
        description='Components Location'
    ),
    'location_dest_id': FieldDefinition(
        name='location_dest_id',
        field_type=FieldType.MANY2ONE,
        relation='stock.location',
        description='Finished Products Location'
    ),
    'state': FieldDefinition(
        name='state',
        field_type=FieldType.SELECTION,
        readonly=True,
        selection_options=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('progress', 'In Progress'),
            ('to_close', 'To Close'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        description='Status'
    ),
    'origin': FieldDefinition(
        name='origin',
        field_type=FieldType.CHAR,
        description='Source Document'
    ),
}


# =============================================================================
# STOCK (stock.quant, stock.move, stock.picking)
# =============================================================================
STOCK_QUANT_FIELDS: Dict[str, FieldDefinition] = {
    'product_id': FieldDefinition(
        name='product_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='product.product',
        description='Product'
    ),
    'location_id': FieldDefinition(
        name='location_id',
        field_type=FieldType.MANY2ONE,
        required=True,
        relation='stock.location',
        description='Location'
    ),
    'lot_id': FieldDefinition(
        name='lot_id',
        field_type=FieldType.MANY2ONE,
        relation='stock.lot',
        description='Lot/Serial Number'
    ),
    'quantity': FieldDefinition(
        name='quantity',
        field_type=FieldType.FLOAT,
        description='Quantity'
    ),
    'reserved_quantity': FieldDefinition(
        name='reserved_quantity',
        field_type=FieldType.FLOAT,
        readonly=True,
        description='Reserved Quantity'
    ),
    'available_quantity': FieldDefinition(
        name='available_quantity',
        field_type=FieldType.FLOAT,
        readonly=True,
        description='Available Quantity'
    ),
}


# =============================================================================
# FWA-SPECIFIC CONFIGURATIONS
# =============================================================================

# Warehouse locations for FWA
FWA_LOCATIONS = {
    'stock': 'WHFWA/Stock',
    'pre_production': 'WHFWA/Pre-Production',
    'subcontracting': 'WHFWA/Subcontracting',
    'input': 'WHFWA/Input',
    'output': 'WHFWA/Output',
}

# Standard fabric consumption per garment (in meters)
# Note: To be refined with CMT partner in Jan 2026
FWA_FABRIC_CONSUMPTION = {
    'golf_shirt_regular': 1.5,  # TBD - confirm with Sandy CMT
    't_shirt': 1.2,
    'polo': 1.5,
    'cap': 0.3,
}

# Product categories for FWA (matches Odoo hierarchy)
FWA_PRODUCT_CATEGORIES = {
    # Root categories
    'goods': 'Goods',
    'imported_goods': 'Imported Goods',
    'raw_material': 'Raw Material',
    'raw_material_imports': 'Raw Material Imports',
    'services': 'Services',
    # Finished Goods subcategories
    'accessories': 'Goods / Accessories',
    'caps': 'Goods / Accessories / Caps',
    'bags': 'Goods / Accessories / Bags',
    'bottoms': 'Goods / Bottoms',
    'trousers': 'Goods / Bottoms / Trousers',
    'outerwear': 'Goods / Outerwear',
    'hoodies': 'Goods / Outerwear / Hoodies',
    'tops': 'Goods / Tops',
    'golf_shirts_local': 'Goods / Tops / Golf Shirts Local CMT',
    't_shirts': 'Goods / Tops / T-Shirts',
    'woven_shirts': 'Goods / Tops / Woven Shirts',
    # Imported Goods
    'golf_shirts_fancy': 'Imported Goods / Golf Shirts Fancy',
    'caps_imported': 'Imported Goods / Caps Imported',
    # Raw Materials
    'fabrics': 'Raw Material / Fabrics',
    'knits': 'Raw Material / Fabrics / Knits',
    'trims': 'Raw Material / Trims',
    'labels': 'Raw Material / Trims / Labels',
    # Services
    'cmt': 'Services / CMT',
    'embroidery': 'Services / Embroidery',
    'printing': 'Services / Printing',
}

# Standard colors (9 colors)
FWA_COLORS = [
    'White', 'Black', 'Red', 'Orange', 'Navy',
    'Blue', 'Green', 'Putty', 'Mayo'
]

# Standard sizes
FWA_SIZES = {
    'mens': ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL', 'XXXXXL'],
    'ladies': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    'kids': ['3-4', '5-6', '7-8', '9-10', '11-12', '13-14'],
    'waist': ['28', '30', '32', '34', '36', '38', '40', '42', '44', '46', '48', '50'],
}

# Key vendors
FWA_VENDORS = {
    'cmt_sandy': {
        'name': 'Sandy CMT',
        'location': 'Zimbabwe',
        'type': 'CMT Manufacturing',
        'products': ['Golf Shirt Regular Men'],
    },
    'rt_knits': {
        'name': 'RT Knits',
        'location': 'Mauritius',
        'type': 'Imported Finished Goods',
        'products': ['Golf Shirt Fancy'],
    },
    'embroidery_dave': {
        'name': 'Embroidery Dave',
        'location': 'Zimbabwe',
        'type': 'Embroidery Services',
    },
    'paramount': {
        'name': 'Paramount Garments Works',
        'location': 'Zimbabwe',
        'type': 'Finished Goods',
        'products': ['Trousers Slim Fit'],
    },
    'african_threads': {
        'name': 'African Threads',
        'location': 'Zimbabwe',
        'type': 'Finished Goods',
        'products': ['T-Shirt Regular'],
    },
}

# CMT Service product (set up as Storable for BOM compatibility)
FWA_CMT_SERVICE = {
    'name': 'CMT Service - Sandy Zimbabwe',
    'type': 'product',  # Storable, NOT service - critical for BOM
    'category': 'Services / CMT',
}


# =============================================================================
# FWA ON THE GO - CUSTOM SALES ORDER FIELDS (Studio Tab)
# =============================================================================
# These fields are added via Odoo Studio to the Sales Order form
# Tab: "FWA on the Go" (after "Other Info" tab)
# Mirrors the legacy Excel tracking system "FWA ON THE GO 2025.xlsx"

# Selection options for x_assigned (Point Man)
FWA_ASSIGNED_OPTIONS = [
    ('bvr', 'BVR'),
    ('mar', 'MAR'),
    ('taf', 'TAF'),
    ('lvr', 'LVR'),
]

# Selection options for x_job_status
FWA_JOB_STATUS_OPTIONS = [
    ('in_progress', 'In Progress'),
    ('on_hold', 'ON HOLD'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('pending_quote', 'Pending Quote'),
    ('pending_fabric', 'Pending Fabric'),
    ('pending_production', 'Pending Production'),
    ('pending_branding', 'Pending Branding'),
    ('pending_payment', 'Pending Payment'),
    ('ready_delivery', 'Ready for Delivery'),
]

# Selection options for x_current_handler
FWA_CURRENT_HANDLER_OPTIONS = [
    ('bvr', 'BVR'),
    ('mar', 'MAR'),
    ('taf', 'TAF'),
    ('lvr', 'LVR'),
    ('cmt', 'At CMT (Sandy)'),
    ('embroidery', 'At Embroidery (Dave)'),
    ('warehouse', 'Warehouse'),
]

# FWA On The Go custom fields for sale.order
FWA_ON_THE_GO_FIELDS: Dict[str, FieldDefinition] = {
    # Order Details - Contact linked to res.partner (child of company)
    # NOTE: x_contact_id replaces x_contact_person and x_mobile
    # The contact's phone/mobile is accessed via the related record
    # Domain filter: [('parent_id', '=', partner_id)] ensures only contacts
    # under the selected company are shown
    'x_contact_id': FieldDefinition(
        name='x_contact_id',
        field_type=FieldType.MANY2ONE,
        relation='res.partner',
        description='Contact person (linked to company contacts in res.partner)'
    ),
    # Related field to display mobile from contact (read-only, auto-populated)
    'x_contact_mobile': FieldDefinition(
        name='x_contact_mobile',
        field_type=FieldType.CHAR,
        readonly=True,
        description='Contact mobile (related field from x_contact_id.mobile)'
    ),
    'x_product_description': FieldDefinition(
        name='x_product_description',
        field_type=FieldType.CHAR,
        description='Free text product description'
    ),
    'x_assigned': FieldDefinition(
        name='x_assigned',
        field_type=FieldType.SELECTION,
        selection_options=FWA_ASSIGNED_OPTIONS,
        description='Staff member responsible (Point Man)'
    ),
    'x_delivery_date': FieldDefinition(
        name='x_delivery_date',
        field_type=FieldType.DATE,
        description='Expected delivery date'
    ),

    # Job Status
    'x_job_status': FieldDefinition(
        name='x_job_status',
        field_type=FieldType.SELECTION,
        selection_options=FWA_JOB_STATUS_OPTIONS,
        description='Current order status'
    ),
    'x_current_handler': FieldDefinition(
        name='x_current_handler',
        field_type=FieldType.SELECTION,
        selection_options=FWA_CURRENT_HANDLER_OPTIONS,
        description='Who is currently working on this order'
    ),

    # Progress Checkboxes (mirrors Excel tracking)
    'x_quotation_check': FieldDefinition(
        name='x_quotation_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Quotation completed'
    ),
    'x_fabric_check': FieldDefinition(
        name='x_fabric_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Fabric sourced/available'
    ),
    'x_mo_check': FieldDefinition(
        name='x_mo_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Manufacturing Order completed'
    ),
    'x_branding_check': FieldDefinition(
        name='x_branding_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Branding/embroidery completed'
    ),
    'x_fiscal_check': FieldDefinition(
        name='x_fiscal_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Fiscal/invoicing completed'
    ),
    'x_payment_check': FieldDefinition(
        name='x_payment_check',
        field_type=FieldType.BOOLEAN,
        default=False,
        description='Payment received'
    ),

    # Notes
    'x_fwa_notes': FieldDefinition(
        name='x_fwa_notes',
        field_type=FieldType.TEXT,
        description='Special instructions / comments'
    ),
}

# Excel to Odoo field mapping for data migration
# NOTE: Contact mapping requires lookup in res.partner to find/create contact under company
FWA_EXCEL_TO_ODOO_MAPPING = {
    'Contact': 'x_contact_id',  # Requires res.partner lookup (Many2one)
    'PointMan': 'x_assigned',
    'DeliveryDate': 'x_delivery_date',
    'Status': 'x_job_status',
    'Product': 'x_product_description',
    'Quotation': 'x_quotation_check',
    'Fabric': 'x_fabric_check',
    'Making': 'x_mo_check',
    'Branding': 'x_branding_check',
    'Fiscal': 'x_fiscal_check',
    'Payment': 'x_payment_check',
    'Notes': 'x_fwa_notes',
}

# Status mapping from Excel to Odoo selection values
FWA_STATUS_MAPPING = {
    'In Progress': 'in_progress',
    'ON HOLD': 'on_hold',
    'Completed': 'completed',
    'Cancelled': 'cancelled',
    'Pending Quote': 'pending_quote',
    'Pending Fabric': 'pending_fabric',
    'Pending Production': 'pending_production',
    'Pending Branding': 'pending_branding',
    'Pending Payment': 'pending_payment',
    'Ready for Delivery': 'ready_delivery',
}

# Point Man mapping (Excel values to Odoo selection values)
FWA_POINTMAN_MAPPING = {
    'BVR': 'bvr',
    'MAR': 'mar',
    'TAF': 'taf',
    'LVR': 'lvr',
}


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_field_value(field_def: FieldDefinition, value: Any) -> tuple[bool, str]:
    """
    Validate a value against a field definition.

    Args:
        field_def: The field definition
        value: The value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required
    if field_def.required and value is None:
        return False, f"Field '{field_def.name}' is required"

    if value is None:
        return True, ""

    # Type checking
    if field_def.field_type == FieldType.INTEGER:
        if not isinstance(value, int):
            return False, f"Field '{field_def.name}' must be an integer"

    elif field_def.field_type == FieldType.FLOAT:
        if not isinstance(value, (int, float)):
            return False, f"Field '{field_def.name}' must be a number"

    elif field_def.field_type == FieldType.BOOLEAN:
        if not isinstance(value, bool):
            return False, f"Field '{field_def.name}' must be a boolean"

    elif field_def.field_type == FieldType.SELECTION:
        if field_def.selection_options:
            valid_values = [opt[0] for opt in field_def.selection_options]
            if value not in valid_values:
                return False, f"Field '{field_def.name}' must be one of: {valid_values}"

    elif field_def.field_type == FieldType.MANY2ONE:
        if not isinstance(value, int):
            return False, f"Field '{field_def.name}' must be a record ID (integer)"

    return True, ""


def get_required_fields(field_definitions: Dict[str, FieldDefinition]) -> List[str]:
    """Get list of required field names from a field definitions dict."""
    return [name for name, field_def in field_definitions.items() if field_def.required]


# =============================================================================
# FIELD DEFINITION EXPORTS (for convenience)
# =============================================================================

FIELD_DEFINITIONS = {
    'res.partner': PARTNER_FIELDS,
    'product.product': PRODUCT_FIELDS,
    'product.template': PRODUCT_FIELDS,  # Similar structure
    'sale.order': SALE_ORDER_FIELDS,
    'sale.order.line': SALE_ORDER_LINE_FIELDS,
    'purchase.order': PURCHASE_ORDER_FIELDS,
    'mrp.production': MANUFACTURING_ORDER_FIELDS,
    'stock.quant': STOCK_QUANT_FIELDS,
}

# Combined sale.order fields (standard + FWA custom)
SALE_ORDER_ALL_FIELDS = {**SALE_ORDER_FIELDS, **FWA_ON_THE_GO_FIELDS}


if __name__ == '__main__':
    # Print field documentation
    print("FWA Odoo Field Mappings")
    print("=" * 60)

    for model, fields in FIELD_DEFINITIONS.items():
        print(f"\n{model}")
        print("-" * 40)
        required = get_required_fields(fields)
        print(f"Required fields: {', '.join(required) if required else 'None'}")
        print(f"Total fields defined: {len(fields)}")
