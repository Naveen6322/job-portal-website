from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    ordering = ("email",)   # ✅ FIX HERE
    list_display = ("email", "role", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Role", {"fields": ("role",)}),
        ("Status", {"fields": ("is_staff", "is_active")}),
        ("Permissions", {"fields": ("is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )

    search_fields = ("email",)   # optional but good
