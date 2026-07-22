from django import forms
from .models import Customer, Vehicle, ServiceVisit, VisitPartUsed


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'owner', 'vehicle_type', 'make_model']


class ServiceVisitForm(forms.ModelForm):
    class Meta:
        model = ServiceVisit
        fields = [
            'vehicle', 
            'senior_technician', 
            'assigned_technicians', 
            'labour_charge', 
            'wheel_alignment', 
            'wheel_balancing', 
            'status'
        ]
        widgets = {
            'assigned_technicians': forms.CheckboxSelectMultiple(),
        }


class VisitPartUsedForm(forms.ModelForm):
    class Meta:
        model = VisitPartUsed
        fields = ['part', 'quantity']
        