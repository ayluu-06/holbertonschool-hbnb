#!/bin/bash

BASE_URL="http://localhost:5000/api/v1/reviews"
USER_URL="http://localhost:5000/api/v1/users"
PLACE_URL="http://localhost:5000/api/v1/places"
AMENITY_URL="http://localhost:5000/api/v1/amenities"

# Crear un nuevo usuario
echo "Creando un nuevo usuario..."
user_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "jchsn.doe@example.com"}' $USER_URL/)
user_id=$(echo "$user_response" | jq -r '.id')
if [ "$user_id" != "null" ]; then
    echo "Usuario creado exitosamente: $user_response"
else
    echo "Error al crear el usuario: $user_response"
    exit 1
fi

# Crear una nueva amenity
echo "Creando una nueva amenity..."
amenity_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "Pool"}' $AMENITY_URL/)
amenity_id=$(echo "$amenity_response" | jq -r '.id')
if [ "$amenity_id" != "null" ]; then
    echo "Amenity creada exitosamente: $amenity_response"
else
    echo "Error al crear la amenity: $amenity_response"
    exit 1
fi

# Crear un nuevo lugar
echo "Creando un nuevo lugar..."
place_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"owner_id": "'$user_id'", "title": "Beach House", "price": 100, "latitude": 40.0, "longitude": -70.0, "description": "A beautiful beach house", "amenities": ["'$amenity_id'"]}' $PLACE_URL/)
place_id=$(echo "$place_response" | jq -r '.id')
if [ "$place_id" != "null" ]; then
    echo "Lugar creado exitosamente: $place_response"
else
    echo "Error al crear el lugar: $place_response"
    exit 1
fi

# Crear una nueva review
echo "Creando una nueva review..."
review_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"user_id": "'$user_id'", "place_id": "'$place_id'", "text": "Amazing place!", "rating": 5}' $BASE_URL/)
if echo "$review_response" | jq -e '.id' &>/dev/null; then
    review_id=$(echo "$review_response" | jq -r '.id')
    echo "Review creada exitosamente: $review_response"
else
    echo "Error al crear la review: $review_response"
    exit 1
fi

# Obtener la review creada
echo "Obteniendo la review con ID: $review_id..."
get_response=$(curl -s -X GET $BASE_URL/$review_id)
if echo "$get_response" | jq -e '.text' &>/dev/null; then
    echo "Review obtenida correctamente: $get_response"
else
    echo "Error al obtener la review: $get_response"
    exit 1
fi

# Eliminar la review
echo "Eliminando la review con ID: $review_id..."
delete_response=$(curl -s -X DELETE $BASE_URL/$review_id)
if echo "$delete_response" | grep -q "success"; then
    echo "Review eliminada exitosamente."
else
    echo "Error al eliminar la review: $delete_response"
    exit 1
fi
