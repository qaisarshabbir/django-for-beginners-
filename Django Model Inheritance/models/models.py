from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Unit(BaseModel):

    name = models.CharField(
        max_length=50
    )

    short_name = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )


class Country(BaseModel):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=10,
        unique=True
    )


class State(BaseModel):

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='states'
    )

    name = models.CharField(
        max_length=100
    )


class City(BaseModel):

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    name = models.CharField(
        max_length=100
    )