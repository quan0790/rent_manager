from django.db.models import Sum, Count
from django.shortcuts import render
from .models import RentInvoice, Tenant
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    print("M-Pesa Callback:", data)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

def dashboard(request):
    total_paid = RentInvoice.objects.filter(is_paid=True).aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    total_unpaid = RentInvoice.objects.filter(is_paid=False).aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    overdue_tenants = Tenant.objects.filter(rentinvoice__is_paid=False, rentinvoice__due_date__lt=timezone.now()).distinct()
    
    context = {
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'overdue_tenants': overdue_tenants,
    }
    return render(request, 'dashboard.html', context)