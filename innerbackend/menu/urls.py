from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, CustomerInformationViewSet, OrderViewSet, upload_menu_image

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'items', MenuItemViewSet, basename='menuitem')
router.register(r'customers', CustomerInformationViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', upload_menu_image, name='upload-menu-image'),
]