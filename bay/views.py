from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Vehicle, ServiceVisit, Part, VisitPartUsed
from .forms import CustomerForm, VehicleForm, ServiceVisitForm, VisitPartUsedForm


# 1. Dashboard View
def dashboard(request):
    total_customers = Customer.objects.count()
    active_visits = ServiceVisit.objects.filter(status='PENDING').count()
    completed_visits = ServiceVisit.objects.filter(status__in=['COMPLETED', 'PAID']).count()
    recent_visits = ServiceVisit.objects.select_related('vehicle').order_by('-visit_date')[:5]

    context = {
        'total_customers': total_customers,
        'active_visits': active_visits,
        'completed_visits': completed_visits,
        'recent_visits': recent_visits,
    }
    return render(request, 'bay/dashboard.html', context)


# 2. Service Visits List
def visit_list(request):
    visits = ServiceVisit.objects.select_related('vehicle', 'vehicle__owner').order_by('-visit_date')
    return render(request, 'bay/visit_list.html', {'visits': visits})


# 3. Create Job Card / Service Visit
def create_visit(request):
    if request.method == 'POST':
        form = ServiceVisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = ServiceVisitForm()
    return render(request, 'bay/visit_form.html', {'form': form})


# 4. Job Card Invoice Detail View
def visit_detail(request, pk):
    visit = get_object_or_404(ServiceVisit, pk=pk)
    
    if request.method == 'POST':
        part_form = VisitPartUsedForm(request.POST)
        if part_form.is_valid():
            visit_part = part_form.save(commit=False)
            visit_part.visit = visit
            visit_part.unit_price = visit_part.part.unit_price
            
            # Inventory Deduction
            part = visit_part.part
            if part.quantity_in_stock >= visit_part.quantity:
                part.quantity_in_stock -= visit_part.quantity
                part.save()
                visit_part.save()
            return redirect('visit_detail', pk=visit.pk)
    else:
        part_form = VisitPartUsedForm()

    return render(request, 'bay/visit_detail.html', {
        'visit': visit,
        'part_form': part_form,
    })


# 5. Create Customer
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_vehicle')
    else:
        form = CustomerForm()
    return render(request, 'bay/customer_form.html', {'form': form})


# 6. Create Vehicle
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_visit')
    else:
        form = VehicleForm()
    return render(request, 'bay/vehicle_form.html', {'form': form})