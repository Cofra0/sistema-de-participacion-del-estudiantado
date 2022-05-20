from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#from .models import CustomUser

# Register your models here.

'''
class CustomUserAdmin(UserAdmin):

    list_display = ("username", "email", "first_name", "last_name", "puntos")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Additional info", {"fields": ("puntos",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
'''