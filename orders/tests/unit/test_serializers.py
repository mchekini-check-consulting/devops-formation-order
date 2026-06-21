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

    def test_invalid_quantity_negative(self):
        data = {"product_id": "prod-1", "quantity": -1, "unit_price": 14.99}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_quantity_one_is_valid(self):
        data = {"product_id": "prod-1", "quantity": 1, "unit_price": 14.99}
        serializer = OrderItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_product_id(self):
        data = {"quantity": 1, "unit_price": 10.00}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_id", serializer.errors)

    def test_missing_unit_price(self):
        data = {"product_id": "prod-1", "quantity": 1}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("unit_price", serializer.errors)

    def test_missing_quantity(self):
        data = {"product_id": "prod-1", "unit_price": 10.00}
        serializer = OrderItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_fields_list(self):
        serializer = OrderItemSerializer()
        expected_fields = {"id", "product_id", "quantity", "unit_price"}
        self.assertEqual(set(serializer.fields.keys()), expected_fields)

    def test_id_is_read_only(self):
        serializer = OrderItemSerializer()
        self.assertTrue(serializer.fields["id"].read_only)

    def test_unit_price_accepts_float(self):
        data = {"product_id": "prod-1", "quantity": 1, "unit_price": 9.99}
        serializer = OrderItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertAlmostEqual(serializer.validated_data["unit_price"], 9.99)


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

    def test_total_price_multiple_items(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 2, "unit_price": 10.00},
                {"product_id": "prod-2", "quantity": 3, "unit_price": 5.00},
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user_id="user-1")
        self.assertEqual(order.total_price, Decimal("35.00"))

    def test_empty_products_list(self):
        data = {"products": []}
        serializer = OrderSerializer(data=data)
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

    def test_user_id_is_read_only(self):
        serializer = OrderSerializer()
        self.assertTrue(serializer.fields["user_id"].read_only)

    def test_total_price_is_read_only(self):
        serializer = OrderSerializer()
        self.assertTrue(serializer.fields["total_price"].read_only)

    def test_status_is_read_only(self):
        serializer = OrderSerializer()
        self.assertTrue(serializer.fields["status"].read_only)

    def test_created_at_is_read_only(self):
        serializer = OrderSerializer()
        self.assertTrue(serializer.fields["created_at"].read_only)

    def test_fields_list(self):
        serializer = OrderSerializer()
        expected_fields = {"id", "user_id", "products", "total_price", "status", "created_at"}
        self.assertEqual(set(serializer.fields.keys()), expected_fields)

    def test_products_maps_to_items_source(self):
        serializer = OrderSerializer()
        self.assertEqual(serializer.fields["products"].source, "items")

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

    def test_serialization_values(self):
        order = Order.objects.create(
            user_id="user-42",
            total_price=Decimal("50.00"),
        )
        OrderItem.objects.create(
            order=order,
            product_id="prod-99",
            quantity=5,
            unit_price=Decimal("10.00"),
        )
        serializer = OrderSerializer(order)
        data = serializer.data
        self.assertEqual(data["user_id"], "user-42")
        self.assertAlmostEqual(float(data["total_price"]), 50.00)
        self.assertEqual(data["status"], "CREATED")
        product = data["products"][0]
        self.assertEqual(product["product_id"], "prod-99")
        self.assertEqual(product["quantity"], 5)
        self.assertAlmostEqual(float(product["unit_price"]), 10.00)

    def test_create_saves_item_fields_correctly(self):
        data = {
            "products": [
                {"product_id": "prod-abc", "quantity": 4, "unit_price": 7.50},
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user_id="user-1")
        item = order.items.first()
        self.assertEqual(item.product_id, "prod-abc")
        self.assertEqual(item.quantity, 4)
        self.assertEqual(item.unit_price, Decimal("7.50"))


class OrderStatusSerializerTest(TestCase):

    def test_valid_status_paid(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "PAID"}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_status_failed(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "FAILED"}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_status_created(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "CREATED"}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_status(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("10.00"),
        )
        serializer = OrderStatusSerializer(order, data={"status": "INVALID"}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_fields_list(self):
        serializer = OrderStatusSerializer()
        expected_fields = {"id", "user_id", "total_price", "status", "created_at"}
        self.assertEqual(set(serializer.fields.keys()), expected_fields)

    def test_read_only_fields(self):
        serializer = OrderStatusSerializer()
        self.assertTrue(serializer.fields["id"].read_only)
        self.assertTrue(serializer.fields["user_id"].read_only)
        self.assertTrue(serializer.fields["total_price"].read_only)
        self.assertTrue(serializer.fields["created_at"].read_only)

    def test_status_is_writable(self):
        serializer = OrderStatusSerializer()
        self.assertFalse(serializer.fields["status"].read_only)

    def test_serialization_output(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("25.00"),
        )
        serializer = OrderStatusSerializer(order)
        data = serializer.data
        self.assertEqual(data["user_id"], "user-1")
        self.assertAlmostEqual(float(data["total_price"]), 25.00)
        self.assertEqual(data["status"], "CREATED")
        self.assertIn("id", data)
        self.assertIn("created_at", data)
