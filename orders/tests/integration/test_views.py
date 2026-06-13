import uuid
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from orders.models import Order, OrderItem


class OrderCreateViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_order_success(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 2, "unit_price": 29.99},
                {"product_id": "prod-2", "quantity": 1, "unit_price": 9.99},
            ]
        }
        response = self.client.post(
            "/api/orders",
            data,
            format="json",
            HTTP_X_USER_ID="user-123",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], "user-123")
        self.assertAlmostEqual(float(response.data["total_price"]), 69.97)
        self.assertEqual(response.data["status"], "CREATED")
        self.assertEqual(len(response.data["products"]), 2)

    def test_create_order_without_user_id_header(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 1, "unit_price": 10.00},
            ]
        }
        response = self.client.post("/api/orders", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user_id", response.data)

    def test_create_order_empty_products(self):
        data = {"products": []}
        response = self.client.post(
            "/api/orders",
            data,
            format="json",
            HTTP_X_USER_ID="user-123",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEqual(float(response.data["total_price"]), 0.0)

    def test_create_order_missing_products(self):
        response = self.client.post(
            "/api/orders",
            {},
            format="json",
            HTTP_X_USER_ID="user-123",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_quantity(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 0, "unit_price": 10.00},
            ]
        }
        response = self.client.post(
            "/api/orders",
            data,
            format="json",
            HTTP_X_USER_ID="user-123",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_saves_to_database(self):
        data = {
            "products": [
                {"product_id": "prod-1", "quantity": 1, "unit_price": 25.00},
            ]
        }
        response = self.client.post(
            "/api/orders",
            data,
            format="json",
            HTTP_X_USER_ID="user-456",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.user_id, "user-456")
        self.assertEqual(order.items.count(), 1)


class OrderListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_orders_empty(self):
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_orders_with_data(self):
        order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("50.00"),
        )
        OrderItem.objects.create(
            order=order,
            product_id="prod-1",
            quantity=5,
            unit_price=Decimal("10.00"),
        )
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]["products"]), 1)


class OrderRetrieveViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("30.00"),
        )
        OrderItem.objects.create(
            order=self.order,
            product_id="prod-1",
            quantity=3,
            unit_price=Decimal("10.00"),
        )

    def test_retrieve_order_success(self):
        response = self.client.get(f"/api/orders/{self.order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.order.id))
        self.assertEqual(response.data["user_id"], "user-1")
        self.assertEqual(len(response.data["products"]), 1)

    def test_retrieve_order_not_found(self):
        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/orders/{fake_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderPatchStatusViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(
            user_id="user-1",
            total_price=Decimal("20.00"),
        )

    def test_patch_status_to_paid(self):
        response = self.client.patch(
            f"/api/orders/{self.order.id}",
            {"status": "PAID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "PAID")
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PAID)

    def test_patch_status_to_failed(self):
        response = self.client.patch(
            f"/api/orders/{self.order.id}",
            {"status": "FAILED"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "FAILED")

    def test_patch_invalid_status(self):
        response = self.client.patch(
            f"/api/orders/{self.order.id}",
            {"status": "INVALID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_not_found(self):
        fake_id = uuid.uuid4()
        response = self.client.patch(
            f"/api/orders/{fake_id}",
            {"status": "PAID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_method_not_allowed(self):
        response = self.client.put(
            f"/api/orders/{self.order.id}",
            {"status": "PAID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_not_allowed(self):
        response = self.client.delete(f"/api/orders/{self.order.id}")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class HealthEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["status"], "UP")
        self.assertEqual(data["service"], "order")
        self.assertIn("timestamp", data)
        self.assertEqual(data["checks"]["database"], "UP")
