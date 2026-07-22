from django.contrib import admin
from .models import Customer, Vehicle, Part, Technician, ServiceVisit, VisitPartUsed


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'phone_number', 'email')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'owner', 'vehicle_type', 'make_model')
    list_filter = ('vehicle_type',)
    search_fields = ('plate_number', 'make_model', 'owner__name')
    autocomplete_fields = ('owner',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit_price', 'quantity_in_stock', 'is_low_stock')
    list_filter = ('category',)
    search_fields = ('name',)

    @admin.display(boolean=True, description='Low Stock')
    def is_low_stock(self, obj):
        return obj.quantity_in_stock <= 5


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_senior')
    list_filter = ('is_senior',)
    search_fields = ('name',)


class VisitPartUsedInline(admin.TabularInline):
    model = VisitPartUsed
    extra = 1


@admin.register(ServiceVisit)
class ServiceVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'visit_date', 'status', 'senior_technician', 'grand_total')
    list_filter = ('status', 'transport_choice')
    search_fields = ('vehicle__plate_number', 'vehicle__owner__name')
    autocomplete_fields = ('vehicle', 'senior_technician')
    filter_horizontal = ('assigned_technicians',)
    inlines = [VisitPartUsedInline]

    @admin.display(description='Grand Total (UGX)')
    def grand_total(self, obj):
        return f"{obj.grand_total:,.0f}"


admin.site.site_header = "Oyera Auto Bay Administration"
admin.site.site_title = "Oyera Auto Bay Admin"
admin.site.index_title = "Records Management"
