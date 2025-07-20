from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.location}"

# 2. Unit model
class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"


class Tenant(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    id_number = models.CharField(max_length=20)
    unit = models.OneToOneField(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    lease_start = models.DateField()
    lease_end = models.DateField()

    def __str__(self):
        return self.full_name

# 4. Rent Invoice model
class RentInvoice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    issued_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice for {self.tenant.full_name} - Due {self.due_date}"

# 5. Payment model
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    invoice = models.ForeignKey(RentInvoice, on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='M-Pesa')
    transaction_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tenant.full_name} - Paid {self.amount_paid}"



