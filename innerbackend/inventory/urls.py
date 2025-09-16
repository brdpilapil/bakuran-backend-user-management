from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, StockTransactionViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'transactions', StockTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
