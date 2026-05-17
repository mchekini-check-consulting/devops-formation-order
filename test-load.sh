#!/bin/bash
# Script de test pour générer des logs variés (création, mise à jour, erreurs)

BASE_URL="http://localhost:8000/api/orders"

echo "=== Test 1: Commande avec 2 produits ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-001" \
  -H "X-User-ID: user-alice" \
  -d '{"user_id": "user-alice", "products": [{"product_id": "prod-1", "quantity": 2, "unit_price": 29.99}, {"product_id": "prod-2", "quantity": 1, "unit_price": 9.99}]}' | python3 -m json.tool

echo ""
echo "=== Test 2: Commande avec 1 produit ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-002" \
  -H "X-User-ID: user-bob" \
  -d '{"user_id": "user-bob", "products": [{"product_id": "prod-42", "quantity": 3, "unit_price": 15.00}]}' | python3 -m json.tool

echo ""
echo "=== Test 3: Commande grosse quantité ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-003" \
  -H "X-User-ID: user-charlie" \
  -d '{"user_id": "user-charlie", "products": [{"product_id": "prod-99", "quantity": 10, "unit_price": 5.50}]}' | python3 -m json.tool

echo ""
echo "=== Test 4: Commande multi-produits ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-004" \
  -H "X-User-ID: user-diana" \
  -d '{"user_id": "user-diana", "products": [{"product_id": "prod-1", "quantity": 1, "unit_price": 100.00}, {"product_id": "prod-2", "quantity": 2, "unit_price": 50.00}, {"product_id": "prod-3", "quantity": 3, "unit_price": 25.00}]}' | python3 -m json.tool

echo ""
echo "=== Test 5: Erreur 400 — body vide ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-005" \
  -H "X-User-ID: user-error" \
  -d '{}' | python3 -m json.tool

echo ""
echo "=== Test 6: Erreur 400 — products manquant ==="
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-006" \
  -d '{"user_id": "user-test"}' | python3 -m json.tool

echo ""
echo "=== Test 7: Erreur 404 — commande inexistante ==="
curl -s -X GET $BASE_URL/00000000-0000-0000-0000-000000000000 \
  -H "X-Correlation-ID: corr-007" | python3 -m json.tool

echo ""
echo "=== Test 8: Lister toutes les commandes ==="
curl -s -X GET $BASE_URL \
  -H "X-Correlation-ID: corr-008" \
  -H "X-User-ID: user-admin" | python3 -m json.tool

echo ""
echo "=== Test 9: PATCH — passer la 1ère commande en PAID ==="
ORDER_ID=$(curl -s -X GET $BASE_URL | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])")
curl -s -X PATCH "$BASE_URL/$ORDER_ID" \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-009" \
  -d '{"status": "PAID"}' | python3 -m json.tool

echo ""
echo "=== Test 10: PATCH — passer en FAILED ==="
ORDER_ID2=$(curl -s -X GET $BASE_URL | python3 -c "import sys,json; print(json.load(sys.stdin)[1]['id'])")
curl -s -X PATCH "$BASE_URL/$ORDER_ID2" \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: corr-010" \
  -d '{"status": "FAILED"}' | python3 -m json.tool

echo ""
echo "=== Terminé — voir les logs avec: docker compose logs app --tail 50 ==="
