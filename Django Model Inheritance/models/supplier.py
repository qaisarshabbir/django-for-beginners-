from django.db import models
from django.contrib.auth.models import User
from .models import (
    BaseModel,
    Country,
    City,
    State,
)

class Supplier(BaseModel):

    supplier_code = models.CharField(
        max_length=50,
        unique=True
    )

    company_name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.SET_NULL
    )

    state = models.ForeignKey(
        State,
        null=True,
        on_delete=models.SET_NULL
    )

    city = models.ForeignKey(
        City,
        null=True,
        on_delete=models.SET_NULL
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )


class SupplierContact(BaseModel):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='contacts'
    )

    name = models.CharField(
        max_length=255
    )

    designation = models.CharField(
        max_length=255,
        blank=True
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    is_primary = models.BooleanField(
        default=False
    )