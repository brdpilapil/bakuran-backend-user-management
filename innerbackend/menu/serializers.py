from rest_framework import serializers
from .models import Category, MenuItem, CustomerInformation, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "category",
            "category_name",
            "price",
            "image",
            "is_available",
            "created_at",
            "updated_at",
        ]

class CustomerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')
    menu_item_price = serializers.ReadOnlyField(source='menu_item.price')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price', 'quantity', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    customer_table = serializers.ReadOnlyField(source='customer.table_number')
    customer_dining_type = serializers.ReadOnlyField(source='customer.dining_type')
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'customer_table', 'customer_dining_type',
            'status', 'total_amount', 'created_at', 'updated_at', 'notes', 'order_items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount']

class CreateOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['customer', 'notes', 'order_items']
    
    def create(self, validated_data):
        print("CreateOrderSerializer - validated_data:", validated_data)
        
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in order_items_data:
            print("Creating order item:", item_data)
            order_item = OrderItem.objects.create(order=order, **item_data)
            total_amount += order_item.subtotal
        
        order.total_amount = total_amount
        order.save()
        
        print(f"Order created: {order.id} with total: {order.total_amount}")
        return order