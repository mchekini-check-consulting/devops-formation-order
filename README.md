# Order Service

Microservice de gestion des commandes pour une application e-commerce.

## Stack

- Python / Django / Django REST Framework
- PostgreSQL (Docker) / SQLite (local)
- Docker + Docker Compose
- Swagger (drf-spectacular)

## Endpoints

| Méthode | URL | Description | Code succès |
|---------|-----|-------------|-------------|
| POST | `/orders/` | Créer une commande | 201 |
| GET | `/orders/` | Lister les commandes | 200 |
| GET | `/orders/<uuid>/` | Détail d'une commande | 200 |

### Payload POST /orders/

```json
{
  "user_id": "user-123",
  "products": [
    { "product_id": "prod-1", "quantity": 2, "unit_price": 29.99 },
    { "product_id": "prod-2", "quantity": 1, "unit_price": 9.99 }
  ]
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
| `.env.local` | Développement local | SQLite |
| `.env.prod` | Docker / Production | PostgreSQL |

Les fichiers `.env` ne sont pas versionnés. Créer les fichiers à partir des exemples ci-dessous.

### .env.local

```
DJANGO_SECRET_KEY=dev-secret-key-local
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DATABASE_ENGINE=sqlite3
CORS_ALLOW_ALL_ORIGINS=True
```

### .env.prod

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=postgresql
POSTGRES_DB=orders_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

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
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
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
