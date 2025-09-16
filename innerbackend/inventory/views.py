from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ingredient, StockTransaction
from .serializers import IngredientSerializer, StockTransactionSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all().order_by('-created_at')
    serializer_class = StockTransactionSerializer

