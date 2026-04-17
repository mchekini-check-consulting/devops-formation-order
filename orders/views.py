from rest_framework import mixins, viewsets, status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .models import Order
from .serializers import OrderSerializer


ORDER_REQUEST_EXAMPLE = OpenApiExample(
    "Commande avec 2 produits",
    value={
        "user_id": "user-123",
        "products": [
            {"product_id": "prod-1", "quantity": 2, "unit_price": 29.99},
            {"product_id": "prod-2", "quantity": 1, "unit_price": 9.99},
        ],
    },
    request_only=True,
)

ORDER_REQUEST_SINGLE = OpenApiExample(
    "Commande avec 1 produit",
    value={
        "user_id": "user-456",
        "products": [
            {"product_id": "prod-42", "quantity": 3, "unit_price": 15.00},
        ],
    },
    request_only=True,
)

ORDER_RESPONSE_EXAMPLE = OpenApiExample(
    "Commande créée",
    value={
        "id": "c7fd3b1e-5e55-460d-8418-6ce8a7e98b2c",
        "user_id": "user-123",
        "total_price": 69.97,
        "status": "CREATED",
        "created_at": "2026-04-17T15:52:21.596297Z",
        "products": [
            {"id": "cf16f2d3-9189-4643-aba9-bc0e07143937", "product_id": "prod-1", "quantity": 2, "unit_price": 29.99},
            {"id": "5cceeb2d-cdc4-45b4-b18d-d2ff18d0ef12", "product_id": "prod-2", "quantity": 1, "unit_price": 9.99},
        ],
    },
    response_only=True,
)

ERROR_400_EXAMPLE = OpenApiExample(
    "Erreur de validation",
    value={
        "products": ["This field is required."]
    },
    response_only=True,
    status_codes=["400"],
)

ERROR_404_EXAMPLE = OpenApiExample(
    "Commande introuvable",
    value={
        "detail": "Not found."
    },
    response_only=True,
    status_codes=["404"],
)


@extend_schema_view(
    create=extend_schema(
        tags=["Commandes"],
        summary="Créer une commande",
        description=(
            "Crée une nouvelle commande avec une liste de produits.\n\n"
            "- Le **total_price** est calculé automatiquement (somme de quantity × unit_price)\n"
            "- Le **status** est automatiquement mis à CREATED\n"
            "- Chaque produit doit contenir : product_id, quantity (≥ 1) et unit_price\n"
        ),
        examples=[ORDER_REQUEST_EXAMPLE, ORDER_REQUEST_SINGLE, ORDER_RESPONSE_EXAMPLE, ERROR_400_EXAMPLE],
        responses={
            201: OpenApiResponse(response=OrderSerializer, description="Commande créée avec succès"),
            400: OpenApiResponse(description="Erreur de validation — champs manquants ou invalides"),
        },
    ),
    list=extend_schema(
        tags=["Commandes"],
        summary="Lister toutes les commandes",
        description="Retourne la liste de toutes les commandes avec leurs items associés.",
        responses={
            200: OpenApiResponse(response=OrderSerializer(many=True), description="Liste des commandes"),
        },
    ),
    retrieve=extend_schema(
        tags=["Commandes"],
        summary="Détail d'une commande",
        description="Retourne le détail d'une commande par son identifiant UUID.",
        examples=[ERROR_404_EXAMPLE],
        responses={
            200: OpenApiResponse(response=OrderSerializer, description="Détail de la commande"),
            404: OpenApiResponse(description="Commande introuvable"),
        },
    ),
)
class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    lookup_field = "pk"
