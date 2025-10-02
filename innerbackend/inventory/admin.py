from django.contrib import admin
from .models import Ingredient, StockTransaction

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "unit")
    search_fields = ("name",)
    list_filter = ("unit",)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "ingredient", "quantity", "transaction_type", "created_at")
    search_fields = ("ingredient__name",)
    list_filter = ("transaction_type", "created_at")
