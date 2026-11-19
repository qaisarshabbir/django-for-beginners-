from django.db import models
from .product import Product

class ProductDetail(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='details'
    )
    
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    dimensions = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    warranty_months = models.IntegerField(default=0)
    
    material = models.CharField(max_length=100, blank=True, null=True)
    
    care_instructions = models.TextField(blank=True, null=True)