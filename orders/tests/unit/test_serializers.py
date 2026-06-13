from decimal import Decimal

from django.test import TestCase

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer, OrderStatusSerializer


class OrderItemSerializerTest(TestCase):

    def test_valid_data(self):
        data = {"product_id": "prod-1", "quantity": 2, "unit_price": 14.99}
        serializer = OrderItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_quantity_zero(self):
        data = {"product_id": "prod-1", "quantity": 0, "unit_price": 14.99}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_missing_product_id(self):
        data = {"quantity": 1, "unit_price": 10.00}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_id", serializer.errors)


class OrderSerializerTest(TestCase):

    def test_valid_create(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 2, "unit_price": 29.99},
                {"product_id": "prod-2", "quantity": 1, "unit_price": 9.99},
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save(user_id="user-1")
        self.assertEqual(order.total_price, Decimal("69.97"))
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.status, Order.Status.CREATED)

    def test_total_price_calculation(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 3, "unit_price": 10.00},
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user_id="user-1")
        self.assertEqual(order.total_price, Decimal("30.00"))

    def test_empty_products_list(self):
        data = {"products": []}
        serializer = OrderSerializer(data=data)
        # DRF accepte une liste vide par défaut, mais le total sera 0
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_products_field(self):
        data = {}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("products", serializer.errors)

    def test_read_only_fields(self):
        data = {
            "user_id": "hacker",
            "total_price": 0.01,
            "status": "PAID",
            "products": [
                {"product_id": "prod-1", "quantity": 1, "unit_price": 100.00},
            ],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save(user_id="real-user")
        self.assertEqual(order.user_id, "real-user")
        self.assertEqual(order.total_price, Decimal("100.00"))
        self.assertEqual(order.status, Order.Status.CREATED)

    def test_serialization_output(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("29.99"),
        )
        OrderItem.objects.create(
            order=order,
            product_id="prod-1",
            quantity=1,
            unit_price=Decimal("29.99"),
        )
        serializer = OrderSerializer(order)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("user_id", data)
        self.assertIn("products", data)
        self.assertIn("total_price", data)
        self.assertIn("status", data)
        self.assertIn("created_at", data)
        self.assertEqual(len(data["products"]), 1)


class OrderStatusSerializerTest(TestCase):

    def test_valid_status_paid(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "PAID"}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_status(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "INVALID"}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
