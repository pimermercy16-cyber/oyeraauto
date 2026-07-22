from django.contrib import admin
from .models import Customer, Vehicle, Part, Technician, ServiceVisit, VisitPartUsed

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Part)
admin.site.register(Technician)
admin.site.register(ServiceVisit)
admin.site.register(VisitPartUsed)