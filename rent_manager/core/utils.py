from datetime import date
from .models import RentalUnit, Invoice
from core.utils import send_invoice_sms
send_invoice_sms("+2547XXXXXXXX", "Hello! Your rent is due. Kindly pay before the due date.")

def generate_monthly_invoices():
    today = date.today()
    generated = 0

    # Loop through all rental units with tenants
    units = RentalUnit.objects.filter(tenant__isnull=False)

    for unit in units:
        # Check if an invoice already exists for the tenant this month
        exists = Invoice.objects.filter(
            tenant=unit.tenant,
            rental_unit=unit,
            due_date__year=today.year,
            due_date__month=today.month
        ).exists()

        if not exists:
            # Create invoice
            Invoice.objects.create(
                tenant=unit.tenant,
                rental_unit=unit,
                amount=unit.monthly_rent,
                due_date=today.replace(day=5),  # Set due date as 5th of the month
                status='Unpaid'
            )
            generated += 1

    return generated
