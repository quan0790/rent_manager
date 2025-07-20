from datetime import date
from core.models import Tenant, Invoice

def generate_monthly_invoices():
    today = date.today()
    tenants = Tenant.objects.all()

    for tenant in tenants:
        # Skip if invoice already exists for this month
        if Invoice.objects.filter(tenant=tenant, due_date__year=today.year, due_date__month=today.month).exists():
            continue

        Invoice.objects.create(
            tenant=tenant,
            amount=tenant.rent_amount,
            due_date=date(today.year, today.month, 5),
            is_paid=False
        )
    print(f"Invoices generated for {today.strftime('%B %Y')}")
