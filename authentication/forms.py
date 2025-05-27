# authentication/forms.py
from django import forms
from .models import ProductCode

class ProductCodeForm(forms.ModelForm):
    class Meta:
        model = ProductCode
        fields = '__all__'  # or list specific fields if you want more control
        exclude = ['code', 'created_at', 'used', 'used_at', 'qr_code_image']  # Exclude fields set by system
