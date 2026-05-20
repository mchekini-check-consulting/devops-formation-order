from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.Status.choices, help_text="Statut de la commande : CREATED, PAID ou FAILED")

    class Meta:
        model = Order
        fields = ["id", "user_id", "total_price", "status", "created_at"]
        read_only_fields = ["id", "user_id", "total_price", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(help_text="Identifiant unique du produit")
    quantity = serializers.IntegerField(help_text="Nombre d'unités commandées", min_value=1)
    unit_price = serializers.FloatField(help_text="Prix unitaire du produit")

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "quantity", "unit_price"]
        read_only_fields = ["id"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, source="items", help_text="Liste des produits de la commande")
    user_id = serializers.CharField(read_only=True, help_text="Identifiant de l'utilisateur (extrait du header X-User-ID)")
    total_price = serializers.FloatField(read_only=True, help_text="Prix total calculé automatiquement")
    status = serializers.CharField(read_only=True, help_text="Statut de la commande : CREATED, PAID ou FAILED")
    created_at = serializers.DateTimeField(read_only=True, help_text="Date et heure de création de la commande")

    class Meta:
        model = Order
        fields = ["id", "user_id", "products", "total_price", "status", "created_at"]
        read_only_fields = ["id", "total_price", "status", "created_at"]

    def create(self, validated_data):
        products_data = validated_data.pop("items")
        total_price = sum(
            Decimal(str(item["unit_price"])) * item["quantity"]
            for item in products_data
        )
        order = Order.objects.create(**validated_data, total_price=total_price)
        for item_data in products_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
