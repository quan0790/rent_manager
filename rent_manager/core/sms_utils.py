import africastalking
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import Invoice

# Initialize Africa's Talking
username = 'sandbox'  # For sandbox use
api_key = 'atsk_34380f42126637bd775fe68e83dab5f147f4ac41cca1c52bc86b5fd9c61177a7ee350e6b'

africastalking.initialize(username, api_key)
sms = africastalking.SMS


def send_invoice_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print("✅ SMS sent:", response)
        return response
    except Exception as e:
        print("❌ Error sending SMS:", str(e))
        return None


def send_sms_reminders_for_unpaid_invoices():
    """
    Sends SMS reminders for unpaid invoices that are due within 3 days or already overdue.
    """
    today = timezone.now().date()
    reminder_threshold = today + timedelta(days=3)

    unpaid_invoices = Invoice.objects.filter(is_paid=False, due_date__lte=reminder_threshold)

    for invoice in unpaid_invoices:
        tenant = invoice.tenant
        phone = tenant.phone_number

        if phone:  # Ensure phone number exists
            message = (
                f"Dear {tenant.name}, your rent of KES {invoice.amount_due} was due on {invoice.due_date}. "
                f"Please make the payment to avoid penalties. Thank you."
            )
            send_invoice_sms(phone, message)
