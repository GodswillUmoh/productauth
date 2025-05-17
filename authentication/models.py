from django.db import models
import uuid

class ProductCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    qr_code_image = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return f"{self.product_name} - {self.code}"

