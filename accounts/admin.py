from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.CustomUser
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_public",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(models.AccountConnection)
class AccountConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "follower",
        "following",
    )
    search_fields = ("user__email",)


admin.site.register(models.CustomUser, CustomUserAdmin)
