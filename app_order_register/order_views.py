from django.views.generic import ListView
from .models import Order  

class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'  
    context_object_name = 'orders'
