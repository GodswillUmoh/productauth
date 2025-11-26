from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ProductCode


# ------------------------------------
# PRODUCT CODE ADMIN
# ------------------------------------
class ProductCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "product_name", "created_at", "is_paid")
    list_filter = ("is_paid", "user")
    search_fields = ("code", "product_name", "user__username")

    actions = ["mark_as_paid"]

    def mark_as_paid(self, request, queryset):
        count = queryset.update(is_paid=True)
        self.message_user(request, f"{count} product codes marked as PAID.")
    mark_as_paid.short_description = "Mark selected as PAID"


admin.site.register(ProductCode, ProductCodeAdmin)


# ------------------------------------
# CUSTOM USER ADMIN WITH STATISTICS
# ------------------------------------
class UserAdmin(BaseUserAdmin):

    list_display = list(BaseUserAdmin.list_display) + [
        "total_codes",
        "paid_codes",
        "unpaid_codes",
    ]

    def total_codes(self, obj):
        return obj.product_codes.count()        # FIXED
    total_codes.short_description = "Total Codes"

    def paid_codes(self, obj):
        return obj.product_codes.filter(is_paid=True).count()     # FIXED
    paid_codes.short_description = "Paid Codes"

    def unpaid_codes(self, obj):
        return obj.product_codes.filter(is_paid=False).count()    # FIXED
    unpaid_codes.short_description = "Unpaid Codes"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
