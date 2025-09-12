from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

# Inline Profile for User admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Custom UserAdmin with filter for unapproved users
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_active', 'get_approved', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'profile__approved')  # Filter by approved
    search_fields = ('username', 'email')

    def get_approved(self, obj):
        return getattr(obj.profile, 'approved', False)
    get_approved.boolean = True
    get_approved.short_description = 'Approved'

    # Optional: only show unapproved users in the admin list
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile').order_by('profile__approved', 'username')

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Optional: standalone Profile admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'user__email')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        # Approve selected users
        for profile in queryset:
            profile.approved = True
            profile.save()
        self.message_user(request, f"{queryset.count()} user(s) approved successfully.")
    approve_users.short_description = "Approve selected users"

# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=Profile)
def activate_user_after_approval(sender, instance, **kwargs):
    if instance.approved and not instance.user.is_active:
        instance.user.is_active = True
        instance.user.save()
