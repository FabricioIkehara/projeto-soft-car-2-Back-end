from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from app_user_register.views import submit_form, getClientById, ClientListView
from app_order_register.views import SubmitOrderView, get_orders, SendEmailView

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit-form/', submit_form, name='submit-form'),
    path('', health_check, name='health_check'),
    path('clients/<int:id>/', getClientById, name='getClientById'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('submit-order/', SubmitOrderView.as_view(), name='submit-order'),
    path('orders/', get_orders, name='get-orders'),
    path('orders/<int:id>/enviar-email/', SendEmailView.as_view(), name='send-email'),  # Nova rota
]