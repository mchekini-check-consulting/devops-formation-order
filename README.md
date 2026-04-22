# Order Service

Microservice de gestion des commandes pour une application e-commerce.

## Stack

- Python / Django / Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Swagger (drf-spectacular)

## Endpoints

| Méthode | URL | Description | Code succès |
|---------|-----|-------------|-------------|
| POST | `/api/orders` | Créer une commande | 201 |
| GET | `/api/orders` | Lister les commandes | 200 |
| GET | `/api/orders/<uuid>` | Détail d'une commande | 200 |
| PATCH | `/api/orders/<uuid>` | Modifier le statut | 200 |

### Payload POST /api/orders

```json
{
  "user_id": "user-123",
  "products": [
    { "product_id": "prod-1", "quantity": 2, "unit_price": 29.99 },
    { "product_id": "prod-2", "quantity": 1, "unit_price": 9.99 }
  ]
}
```

### Payload PATCH /api/orders/<uuid>

```json
{
  "status": "PAID"
}
```

## Lancement en local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

L'API est disponible sur http://127.0.0.1:8000

Insérer des données de test (serveur lancé) :

```bash
chmod +x seed.sh
./seed.sh
```

## Lancement avec Docker

```bash
docker-compose up --build
```

L'API est disponible sur http://127.0.0.1:8000

## Documentation Swagger

http://127.0.0.1:8000/api/docs/

## Gestion des environnements

| Fichier | Environnement | Base de données |
|---------|---------------|-----------------|
| `.env.local` | Développement local | PostgreSQL (localhost) |
| `.env.prod` | Docker / Production | PostgreSQL (db) |

## Structure du projet

```
order-service/
├── .env.local
├── .env.prod
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── seed.sh
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
└── orders/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── migrations/
```
