from rest_framework import serializers
from .models import Ingredient, StockTransaction

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class StockTransactionSerializer(serializers.ModelSerializer):
    # Show ingredient details instead of just ID
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient', write_only=True
    )

    class Meta:
        model = StockTransaction
        fields = ['id', 'ingredient', 'ingredient_id', 'transaction_type', 'quantity', 'note', 'created_at']

    def create(self, validated_data):
        ingredient = validated_data["ingredient"]
        qty = validated_data["quantity"]
        tx_type = validated_data["transaction_type"]

        # Apply stock logic here
        if tx_type == "IN":
            ingredient.quantity += qty
        elif tx_type == "OUT":
            if ingredient.quantity < qty:
                raise serializers.ValidationError(
                    {"detail": f"Not enough stock of {ingredient.name}"}
                )
            ingredient.quantity -= qty
        elif tx_type == "ADJ":
            ingredient.quantity = qty

        # Save updated stock
        ingredient.save(update_fields=["quantity"])

        # Save the transaction record
        return super().create(validated_data)
