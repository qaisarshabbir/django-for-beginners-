from django.contrib.auth.models import User
from django.db import models
from .models import (
    BaseModel,
    Unit
)
from .category import Category
from .brand import Brand
from .supplier import Supplier
from .tax import Tax

# Create your models here.
class Product(BaseModel):

    class ProductType(models.TextChoices):
        STOCK = "stock", "Stock Product"
        SERVICE = "service", "Service"
        DIGITAL = "digital", "Digital"

    sku = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique Stock Keeping Unit"
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )

    name = models.CharField(
        max_length=255,
        db_index=True
    )

    slug = models.SlugField(
        unique=True
    )

    short_description = models.CharField(
        max_length=500,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products"
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="products"
    )

    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products"
    )

    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.STOCK
    )

    cost_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    selling_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    wholesale_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    current_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    minimum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    maximum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    reorder_level = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    allow_backorder = models.BooleanField(
        default=False
    )

    has_serial_number = models.BooleanField(
        default=False
    )

    has_expiry_date = models.BooleanField(
        default=False
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="products_created"
    )

    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products_updated"
    )

    class Meta:
        # ordering = ["name"]
        # Descending:
        # ordering = ['-created_at']

        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name



class ProductImage(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    is_primary = models.BooleanField(
        default=False
    )

    display_order = models.PositiveIntegerField(
        default=0
    )


class ProductDocument(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="product_documents/"
    )


class ProductSupplier(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="suppliers"
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products"
    )

    supplier_sku = models.CharField(
        max_length=100,
        blank=True
    )

    purchase_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    lead_time_days = models.PositiveIntegerField(
        default=0
    )

    is_default = models.BooleanField(
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "supplier"],
                name="unique_product_supplier"
            )
        ]