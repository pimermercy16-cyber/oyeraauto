from django import forms
from .models import Customer, Vehicle, ServiceVisit, VisitPartUsed, Part, Technician

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'address']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['owner', 'plate_number', 'make_model', 'vehicle_type']

class ServiceVisitForm(forms.ModelForm):
    class Meta:
        model = ServiceVisit
        fields = [
            'vehicle', 
            'senior_technician', 
            'assigned_technicians', 
            'issue_description', 
            'transport_choice',
            'wheel_alignment', 
            'wheel_balancing', 
            'computer_diagnostics', 
            'oil_change_service', 
            'brake_service', 
            'suspension_check', 
            'ac_servicing', 
            'labour_charge', 
            'status'
        ]
        widgets = {
            'assigned_technicians': forms.CheckboxSelectMultiple(),
            'issue_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe the issue or state if unsure what is wrong...'}),
            'transport_choice': forms.Select(attrs={'class': 'form-select'}),
        }

class VisitPartUsedForm(forms.ModelForm):
    class Meta:
        model = VisitPartUsed
        fields = ['part', 'quantity'] # Exclude 'visit' and 'unit_price' so validation passes cleanly

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'category', 'unit_price', 'quantity_in_stock']

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'phone_number', 'is_senior']

        