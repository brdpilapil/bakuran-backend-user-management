from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In (Purchase)'),
        ('OUT', 'Stock Out (Usage)'),
        ('ADJ', 'Adjustment'),
    ]

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.ingredient.unit} of {self.ingredient.name}"
