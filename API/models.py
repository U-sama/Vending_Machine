from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_product_cost(value):
    if value % 5 != 0 :
        raise ValidationError('Value must be multiplier of 5.')


class Users(AbstractUser):
    deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Product(models.Model):
    productName = models.CharField(max_length=100)
    amountAvailable = models.IntegerField(default=0)
    cost = models.IntegerField(validators= [validate_product_cost])
    seller = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True)