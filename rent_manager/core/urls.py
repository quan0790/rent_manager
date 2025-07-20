from django.urls import path
from .views import mpesa_callback, dashboard
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.mpesa_utils import lipa_na_mpesa
urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('dashboard/', dashboard, name='dashboard'),
]
@login_required
def pay_rent(request):
    tenant = request.user.tenant
    response = lipa_na_mpesa(tenant.phone_number, tenant.rent_amount)
    return JsonResponse(response)
