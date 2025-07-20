from django.contrib import admin
from .models import RentalUnit, Tenant, Invoice
from .utils import generate_monthly_invoices
from django.contrib import messages

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'rental_unit', 'amount', 'due_date', 'status')
    actions = ['generate_invoices']

    def generate_invoices(self, request, queryset):
        count = generate_monthly_invoices()
        self.message_user(request, f"{count} invoice(s) generated successfully.", level=messages.SUCCESS)

    generate_invoices.short_description = "Generate Monthly Invoices for All Tenants"
