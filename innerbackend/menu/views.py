from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Prefetch
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.pagination import PageNumberPagination
from .models import Category, MenuItem, CustomerInformation, Order, OrderItem
from .serializers import (
    CategorySerializer, MenuItemSerializer, CustomerInformationSerializer,
    OrderSerializer, CreateOrderSerializer
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_menu_image(request):
    try:
        image_data = request.data.get('image')
        filename = request.data.get('filename', f'menu_item_{uuid.uuid4()}.jpg')
        
        if not image_data:
            return Response({'error': 'No image data provided'}, status=400)
        
        # Extract base64 data
        if ';base64,' in image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
        else:
            imgstr = image_data
            ext = 'jpg'
        
        # Ensure filename has proper extension
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filename = f"{filename}.jpg"
        
        # Decode base64
        image_file = ContentFile(base64.b64decode(imgstr), name=filename)
        
        # Save to media storage
        from django.core.files.storage import default_storage
        file_path = default_storage.save(f'menu_images/{filename}', image_file)
        
        # Return relative path instead of absolute URL
        # This will be: 'media/menu_images/filename.jpg'
        relative_url = f'/media/{file_path}'
        
        print(f"Image uploaded to: {file_path}")
        return Response({
            'url': relative_url,
            'file_path': file_path,
            'filename': filename
        })
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return Response({'error': str(e)}, status=500)

class OrderPagination(PageNumberPagination):
    page_size = 5  # Number of orders per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all().order_by("name")
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CustomerInformationViewSet(viewsets.ModelViewSet):
    queryset = CustomerInformation.objects.all()
    serializer_class = CustomerInformationSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer').prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.select_related('menu_item'))
    ).all().order_by('-created_at')  # Order by newest first
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    # Add filtering by status
    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def list(self, request, *args, **kwargs):
        print(f"Order list request - Page: {request.GET.get('page')}, Status: {request.GET.get('status')}")
        print(f"Total orders: {self.get_queryset().count()}")
        return super().list(request, *args, **kwargs)

    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
    
        print(f"Updating order {order.id} from {order.status} to {new_status}")
    
        if new_status in dict(Order.ORDER_STATUS_CHOICES):
            order.status = new_status
            order.save()
            print(f"Order {order.id} status updated to {order.status}")
            return Response({'status': 'Status updated successfully'})
    
        print(f"Invalid status: {new_status}")
        return Response(
            {'error': 'Invalid status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = self.queryset.filter(status=status_filter)
        else:
            orders = self.queryset
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    # Add order statistics
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Use more efficient database aggregation
        from django.db.models import Count, Q
        
        stats = Order.objects.aggregate(
            total_orders=Count('id'),
            pending_orders=Count('id', filter=Q(status='PENDING')),
            preparing_orders=Count('id', filter=Q(status='PREPARING')),
            completed_orders=Count('id', filter=Q(status='COMPLETED'))
        )
        
        return Response(stats)