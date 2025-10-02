from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_blocked")
    search_fields = ("username", "email")
    list_filter = ("role", "is_blocked")
    ordering = ("id",)
