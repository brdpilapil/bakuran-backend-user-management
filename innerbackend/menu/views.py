from django.shortcuts import render
from rest_framework import viewsets
from backend.innerbackend.menu.models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend.innerbackend.menu.models import MenuItem
from .serializers import MenuItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by("name")
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]