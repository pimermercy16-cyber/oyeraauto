from django.test import TestCase
from django.urls import reverse
from .models import Customer, Vehicle, Technician, Part, ServiceVisit, VisitPartUsed


class ServiceVisitPricingTests(TestCase):
    """Confirms the pricing logic in models.py matches the brief:
    labour (20,000) + selected services + parts used."""

    def setUp(self):
        self.customer = Customer.objects.create(name="Grace Nakato", phone_number="0700123456")
        self.vehicle = Vehicle.objects.create(
            plate_number="UBA 123X", owner=self.customer, vehicle_type="SMALL"
        )
        self.part = Part.objects.create(
            name="Engine Oil 5W-30", category="ENGINE_OIL",
            unit_price=120000, quantity_in_stock=10
        )

    def test_default_labour_charge_only(self):
        visit = ServiceVisit.objects.create(vehicle=self.vehicle)
        self.assertEqual(visit.total_service_charges, 20000)
        self.assertEqual(visit.grand_total, 20000)

    def test_wheel_alignment_and_balancing_add_correctly(self):
        visit = ServiceVisit.objects.create(
            vehicle=self.vehicle, wheel_alignment=True, wheel_balancing=True
        )
        # 20,000 labour + 30,000 alignment + 20,000 balancing
        self.assertEqual(visit.total_service_charges, 70000)

    def test_parts_used_add_to_grand_total(self):
        visit = ServiceVisit.objects.create(vehicle=self.vehicle)
        VisitPartUsed.objects.create(
            visit=visit, part=self.part, quantity=2, unit_price=self.part.unit_price
        )
        self.assertEqual(visit.total_parts_cost, 240000)
        self.assertEqual(visit.grand_total, 260000)  # 20,000 labour + 240,000 parts

    def test_multiple_technicians_can_be_assigned(self):
        t1 = Technician.objects.create(name="Moses Okello", is_senior=True)
        t2 = Technician.objects.create(name="Sarah Auma")
        visit = ServiceVisit.objects.create(vehicle=self.vehicle, senior_technician=t1)
        visit.assigned_technicians.set([t1, t2])
        self.assertEqual(visit.assigned_technicians.count(), 2)


class InventoryStockTests(TestCase):
    """Confirms stock cannot be reduced below zero and deducts correctly."""

    def setUp(self):
        self.customer = Customer.objects.create(name="Grace Nakato", phone_number="0700123456")
        self.vehicle = Vehicle.objects.create(
            plate_number="UBA 123X", owner=self.customer, vehicle_type="SMALL"
        )
        self.visit = ServiceVisit.objects.create(vehicle=self.vehicle)
        self.part = Part.objects.create(
            name="Oil Filter", category="OIL_FILTER", unit_price=18000, quantity_in_stock=3
        )

    def test_stock_deducts_via_view_when_sufficient(self):
        self.client.post(
            reverse('visit_detail', args=[self.visit.pk]),
            {'part': self.part.pk, 'quantity': 2}
        )
        self.part.refresh_from_db()
        self.assertEqual(self.part.quantity_in_stock, 1)

    def test_stock_not_deducted_when_insufficient(self):
        self.client.post(
            reverse('visit_detail', args=[self.visit.pk]),
            {'part': self.part.pk, 'quantity': 10}
        )
        self.part.refresh_from_db()
        self.assertEqual(self.part.quantity_in_stock, 3)  # unchanged
        self.assertEqual(self.visit.parts_used.count(), 0)


class CoreViewsRenderTests(TestCase):
    """Smoke tests: every core page should render without error."""

    def setUp(self):
        self.customer = Customer.objects.create(name="Grace Nakato", phone_number="0700123456")
        self.vehicle = Vehicle.objects.create(
            plate_number="UBA 123X", owner=self.customer, vehicle_type="SMALL"
        )
        self.visit = ServiceVisit.objects.create(vehicle=self.vehicle)

    def test_pages_return_200(self):
        urls = [
            reverse('dashboard'),
            reverse('customer_list'),
            reverse('create_customer'),
            reverse('create_vehicle'),
            reverse('visit_list'),
            reverse('create_visit'),
            reverse('visit_detail', args=[self.visit.pk]),
            reverse('part_list'),
            reverse('create_part'),
            reverse('technician_list'),
            reverse('create_technician'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"{url} did not return 200")
