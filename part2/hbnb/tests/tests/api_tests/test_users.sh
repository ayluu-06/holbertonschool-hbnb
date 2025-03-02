#!/bin/bash

echo "Creando usuario..."
curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "Roberto",
    "last_name": "Gonzales",
    "email": "roberto@example.com"
}' | jq

echo ""
echo "Intentando crear usuario con datos inválidos..."
curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}' | jq

echo ""
echo ""
echo "Obteniendo lista de usuarios..."
curl -s -X GET "http://127.0.0.1:5000/api/v1/users/" | jq