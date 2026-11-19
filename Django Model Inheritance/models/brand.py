from django.db import models
from .models import BaseModel

class Brand(BaseModel):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to='brands/',
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
            return self.name