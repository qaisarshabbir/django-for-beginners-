from django.contrib import admin
from .models.brand import Brand
from .models.product import ( 
    ProductImage, 
    ProductDocument 
)
from .models import (
    Category,
    Product,
    ProductDetail,
    Supplier,
    Tax
)
# Register your models here.
# admin.site.register(Brand)
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'description',
            'is_active',
        )

# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'slug',
            'description',
            'is_active',
        )

# admin.site.register(Products)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'selling_price',
            'description',
            'product_type',
        )
    search_fields = ['name', 'description']
    list_filter = ['product_type']
    ordering = ['-name']
    list_per_page = 25
    list_display_links = ['selling_price', 'description']

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'classes': ('collapse',),
            'fields': ('name', 'sku', 'slug', 'short_description', 'description', 'notes')
        }),
        ('Categories & Organization', {
            'classes': ('collapse',),
            'fields': ('brand', 'category', 'barcode', 'unit', 'tax')
        }),
        ('Pricing & Inventory', {
            'fields': ('cost_price', 'selling_price', 'wholesale_price', 'minimum_stock', 'maximum_stock', 'reorder_level')
        }),
        ('Attributes', {
            'fields': ('weight', 'length', 'width', 'height', 'image')
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_active', 'allow_backorder', 'has_serial_number', 'has_expiry_date', 'product_type')
        }),
        ('Dates & Users', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at')
        }),
    )

# admin.site.register(ProductDetail)
@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Supplier)
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
            'company_name',
            'supplier_code',
            'phone',
            'email',
        )

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass