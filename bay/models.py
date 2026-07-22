from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


# 1. Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)    
    address = models.TextField(blank=True, null=True)   

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# 2. Vehicle Model
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('SMALL', 'Small Car'),
        ('COMMERCIAL', 'Commercial Car'),
        ('HEAVY', 'Heavy Vehicle'),
    ]
    plate_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='SMALL')
    make_model = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.plate_number} - {self.get_vehicle_type_display()}"


# 3. Spare Parts & Fluids Inventory Model
class Part(models.Model):
    CATEGORY_CHOICES = [
        ('ENGINE_OIL', 'Engine Oil'),
        ('GEARBOX_OIL', 'Gearbox Oil'),
        ('BRAKE_FLUID', 'Brake Fluid'),
        ('OIL_FILTER', 'Oil Filter'),
        ('OTHER_FILTER', 'Other Filter'),
        ('BRAKE_PADS', 'Brake Pads'),
        ('MISC', 'Miscellaneous Part'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # In UGX
    quantity_in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.unit_price} UGX ({self.quantity_in_stock} in stock)"


# 4. Technician Model
class Technician(models.Model):
    name = models.CharField(max_length=100)
    is_senior = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        role = "Senior Technician" if self.is_senior else "Technician"
        return f"{self.name} ({role})"


# 5. Service Visit / Job Card Model
class ServiceVisit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'In Service Bay'),
        ('LOGISTICS_PENDING', 'Pending Pickup/Arrival'),
        ('COMPLETED', 'Completed'),
        ('PAID', 'Paid & Released'),
    ]
    
    TRANSPORT_CHOICES = [
        ('CUSTOMER_BRINGING', 'Customer will bring car to service bay'),
        ('BAY_PICKUP_TOW', 'Service bay to fix/tow from current location'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(auto_now_add=True)
    senior_technician = models.ForeignKey(
        Technician, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspected_jobs'
    )
    assigned_technicians = models.ManyToManyField(Technician, blank=True, related_name='service_jobs')
    
    # Customer Issue & Logistics Options
    issue_description = models.TextField(blank=True, null=True, help_text="Describe the problem, or state if unsure what's wrong.")
    transport_choice = models.CharField(max_length=50, choices=TRANSPORT_CHOICES, default='CUSTOMER_BRINGING')

    # Comprehensive Service Checkboxes & Charges (in UGX)
    labour_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('20000.00'))
    wheel_alignment = models.BooleanField(default=False)       # 30,000 UGX
    wheel_balancing = models.BooleanField(default=False)       # 20,000 UGX
    computer_diagnostics = models.BooleanField(default=False)  # 50,000 UGX
    oil_change_service = models.BooleanField(default=False)    # 40,000 UGX
    brake_service = models.BooleanField(default=False)         # 40,000 UGX
    suspension_check = models.BooleanField(default=False)      # 30,000 UGX
    ac_servicing = models.BooleanField(default=False)          # 60,000 UGX
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')

    @property
    def total_service_charges(self):
        total = self.labour_charge
        if self.wheel_alignment:
            total += 30000
        if self.wheel_balancing:
            total += 20000
        if self.computer_diagnostics:
            total += 50000
        if self.oil_change_service:
            total += 40000
        if self.brake_service:
            total += 40000
        if self.suspension_check:
            total += 30000
        if self.ac_servicing:
            total += 60000
        return total

    @property
    def total_parts_cost(self):
        return sum(item.subtotal for item in self.parts_used.all())

    @property
    def grand_total(self):
        return self.total_service_charges + self.total_parts_cost

    def __str__(self):
        return f"Visit #{self.id} - {self.vehicle.plate_number} on {self.visit_date.strftime('%Y-%m-%d')}"


# 6. Parts Used per Service Visit
class VisitPartUsed(models.Model):
    visit = models.ForeignKey(ServiceVisit, on_delete=models.CASCADE, related_name='parts_used')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.part.name} for Visit #{self.visit.id}"