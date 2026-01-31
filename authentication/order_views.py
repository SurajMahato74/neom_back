from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Order, OrderItem
from .order_serializers import OrderSerializer, OrderCreateSerializer
import urllib.parse

class OrderCreateView(generics.CreateAPIView):
    """Public endpoint to create orders"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Generate WhatsApp message
            whatsapp_message = self.generate_whatsapp_message(order)
            whatsapp_url = f"https://wa.me/9779851476666?text={urllib.parse.quote(whatsapp_message)}"
            
            return Response({
                'message': 'Order created successfully!',
                'order_id': order.id,
                'whatsapp_url': whatsapp_url
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def generate_whatsapp_message(self, order):
        message = f"🛒 *New Order #{order.id}*\n\n"
        message += f"👤 *Customer:* {order.customer_name}\n"
        message += f"📱 *Phone:* {order.customer_phone}\n"
        if order.customer_email:
            message += f"📧 *Email:* {order.customer_email}\n"
        message += f"📍 *Address:* {order.delivery_address}\n\n"
        
        message += "*📦 Order Items:*\n"
        for item in order.items.all():
            message += f"• {item.product.name}\n"
            message += f"  Qty: {item.quantity} | Price: Rs. {item.unit_price} | Total: Rs. {item.total_price}\n\n"
        
        message += f"💰 *Total Amount: Rs. {order.total_amount}*\n\n"
        
        if order.notes:
            message += f"📝 *Notes:* {order.notes}\n\n"
        
        message += "Please confirm this order. Thank you!"
        
        return message

# Admin Views
class OrderManagementListView(generics.ListAPIView):
    """Admin endpoint to view all orders"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.all()
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if search:
            queryset = queryset.filter(
                Q(customer_name__icontains=search) |
                Q(customer_phone__icontains=search) |
                Q(id__icontains=search)
            )
        
        return queryset

class OrderManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to manage individual orders"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer