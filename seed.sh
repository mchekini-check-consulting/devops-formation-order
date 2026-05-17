#!/bin/sh

URL="http://localhost:8000/api/orders"

curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"user_id":"user-101","products":[{"product_id":"prod-1","quantity":2,"unit_price":29.99},{"product_id":"prod-2","quantity":1,"unit_price":9.99}]}'
echo

curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"user_id":"user-102","products":[{"product_id":"prod-3","quantity":1,"unit_price":49.99}]}'
echo

curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"user_id":"user-103","products":[{"product_id":"prod-1","quantity":3,"unit_price":29.99},{"product_id":"prod-4","quantity":2,"unit_price":15.00}]}'
echo

curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"user_id":"user-104","products":[{"product_id":"prod-5","quantity":1,"unit_price":99.99},{"product_id":"prod-2","quantity":4,"unit_price":9.99}]}'
echo

curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"user_id":"user-105","products":[{"product_id":"prod-3","quantity":2,"unit_price":49.99},{"product_id":"prod-1","quantity":1,"unit_price":29.99},{"product_id":"prod-5","quantity":1,"unit_price":99.99}]}'
echo
