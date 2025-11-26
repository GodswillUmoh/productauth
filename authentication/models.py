from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

class ProductCode(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='product_codes', null=True,  blank=True)
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    nafdac_no = models.CharField(max_length=50, default='101')
    date_produced = models.DateField(default=datetime.date(2024, 1, 1))
    date_expired = models.DateField(default=datetime.date(2025, 5, 26))
    location_manufactured = models.CharField(max_length=255, default='Lagos')
    ingredients = models.TextField(default='Not Available')
    is_paid = models.BooleanField(default=False)


    from django.contrib.auth.models import User

 


    def __str__(self):
        return f"{self.product_name} - {self.code}"
