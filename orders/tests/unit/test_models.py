import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from orders.models import Order, OrderItem


class OrderModelTest(TestCase):

    def test_create_order_with_defaults(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("59.98"),
        )
        self.assertEqual(order.user_id, "user-1")
        self.assertEqual(order.total_price, Decimal("59.98"))
        self.assertEqual(order.status, Order.Status.CREATED)
        self.assertIsInstance(order.id, uuid.UUID)
        self.assertIsNotNone(order.created_at)

    def test_order_status_choices(self):
        self.assertEqual(Order.Status.CREATED, "CREATED")
        self.assertEqual(Order.Status.PAID, "PAID")
        self.assertEqual(Order.Status.FAILED, "FAILED")

    def test_order_status_update(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        order.status = Order.Status.PAID
        order.save()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)

    def test_order_str_representation(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        # Le modèle n'a pas de __str__ custom, on vérifie juste que ça ne crash pas
        str(order)


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("29.99"),
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product_id="prod-1",
            quantity=2,
            unit_price=Decimal("14.99"),
        )
        self.assertEqual(item.product_id, "prod-1")
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Decimal("14.99"))
        self.assertIsInstance(item.id, uuid.UUID)

    def test_order_item_related_name(self):
        OrderItem.objects.create(
            order=self.order,
            product_id="prod-1",
            quantity=1,
            unit_price=Decimal("10.00"),
        )
        OrderItem.objects.create(
            order=self.order,
            product_id="prod-2",
            quantity=3,
            unit_price=Decimal("5.00"),
        )
        self.assertEqual(self.order.items.count(), 2)

    def test_order_item_cascade_delete(self):
        OrderItem.objects.create(
            order=self.order,
            product_id="prod-1",
            quantity=1,
            unit_price=Decimal("10.00"),
        )
        order_id = self.order.id
        self.order.delete()
        self.assertEqual(OrderItem.objects.filter(order_id=order_id).count(), 0)

    def test_order_item_quantity_min_validator(self):
        item = OrderItem(
            order=self.order,
            product_id="prod-1",
            quantity=0,
            unit_price=Decimal("10.00"),
        )
        with self.assertRaises(ValidationError):
            item.full_clean()
