from django import forms
from .models import Customer, Vehicle, ServiceVisit, Part, VisitPartUsed


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0771234567'}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'owner', 'vehicle_type', 'make_model']
        widgets = {
            'plate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. UBB 123X'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'make_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Toyota Fielder'}),
        }


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
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'senior_technician': forms.Select(attrs={'class': 'form-select'}),
            'assigned_technicians': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'labour_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'UGX Amount'}),
            'wheel_alignment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wheel_balancing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class VisitPartUsedForm(forms.ModelForm):
    class Meta:
        model = VisitPartUsed
        fields = ['part', 'quantity']
        widgets = {
            'part': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'unit_price', 'quantity_in_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Part Name (e.g. Engine Oil 5L)'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in UGX'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity in Stock'}),
        }