from django.db import models
from .models import (
    BaseModel,
)

class Tax(BaseModel):

    name = models.CharField(
        max_length=100
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )