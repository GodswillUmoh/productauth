from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile
from authentication.models import ProductCode  # adjust path if needed


# ------------------------------
# PROFILE INLINE
# ------------------------------
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


# ------------------------------
# MERGED USER ADMIN
# ------------------------------
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    list_display = (
        'username', 'email', 'is_active', 'get_approved',
        'total_codes', 'paid_codes', 'unpaid_codes', 'is_staff'
    )

    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 'profile__approved'
    )

    search_fields = ('username', 'email')

    def get_approved(self, obj):
        return getattr(obj.profile, 'approved', False)
    get_approved.boolean = True
    get_approved.short_description = 'Approved'

    # ------------------------------
    # PRODUCT CODE STATS
    # ------------------------------
    def total_codes(self, obj):
        return obj.product_codes.count()
    total_codes.short_description = "Total Codes"

    def paid_codes(self, obj):
        return obj.product_codes.filter(is_paid=True).count()
    paid_codes.short_description = "Paid Codes"

    def unpaid_codes(self, obj):
        return obj.product_codes.filter(is_paid=False).count()
    unpaid_codes.short_description = "Unpaid Codes"


# ------------------------------
# REGISTER MERGED USER ADMIN
# ------------------------------
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ------------------------------
# PROFILE ADMIN (OPTIONAL)
# ------------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'user__email')

    def approve_users(self, request, queryset):
        for profile in queryset:
            profile.approved = True
            profile.save()
        self.message_user(request, f"{queryset.count()} user(s) approved successfully.")
