#!/bin/bash

BASE_URL="http://localhost:5000/api/v1/places"
BASE_URL_USERS="http://localhost:5000/api/v1/users"
BASE_URL_AMENITIES="http://localhost:5000/api/v1/amenities"

# Crear un nuevo usuario (owner) si no existe
echo "Creando un nuevo usuario..."
create_user_response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"email": "ejemplo12@example.com", "first_name": "Juan", "last_name": "Pérez"}' $BASE_URL_USERS/)
http_code=$(echo "$create_user_response" | tail -n 1)  # Obtener el código de estado HTTP
create_user_response_body=$(echo "$create_user_response" | head -n -1)  # Obtener el cuerpo de la respuesta

echo "Respuesta de crear usuario: $create_user_response_body"  # Agregado para depuración
echo "Código de estado HTTP al crear usuario: $http_code"

if echo "$create_user_response_body" | jq -e '.id' &>/dev/null; then
    owner_id=$(echo "$create_user_response_body" | jq -r '.id')
    echo "Usuario creado exitosamente con ID: $owner_id"
else
    echo "Error al crear el usuario: $create_user_response_body"
    exit 1
fi

# Crear amenities si no existen
echo "Creando amenities..."
create_amenity1_response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"name": "wifi"}' $BASE_URL_AMENITIES/)
create_amenity2_response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"name": "estacionamiento"}' $BASE_URL_AMENITIES/)

# Obtener los códigos de estado y las respuestas
http_code_amenity1=$(echo "$create_amenity1_response" | tail -n 1)
http_code_amenity2=$(echo "$create_amenity2_response" | tail -n 1)
amenity1_response_body=$(echo "$create_amenity1_response" | head -n -1)
amenity2_response_body=$(echo "$create_amenity2_response" | head -n -1)

echo "Respuesta de crear amenity1: $amenity1_response_body"
echo "Código de estado HTTP para amenity1: $http_code_amenity1"
echo "Respuesta de crear amenity2: $amenity2_response_body"
echo "Código de estado HTTP para amenity2: $http_code_amenity2"

amenity1_id=$(echo "$amenity1_response_body" | jq -r '.id')
amenity2_id=$(echo "$amenity2_response_body" | jq -r '.id')

echo "Amenity1 creado con ID: $amenity1_id"
echo "Amenity2 creado con ID: $amenity2_id"

# Verificar el valor de owner_id
echo "owner_id a enviar: $owner_id"  # Línea de depuración

# Crear un lugar con datos válidos y mostrar la solicitud completa
echo "Creando un nuevo lugar con datos válidos..."
create_place_request='{
    "title": "La costa ", 
    "description": "Lugar tranquilo ", 
    "price": 1000, 
    "latitude": 80, 
    "longitude": -56, 
    "owner_id": "'"$owner_id"'", 
    "amenities": [
        "'"$amenity1_id"'",
        "'"$amenity2_id"'"
    ]
}'
echo "Solicitud de creación de lugar: $create_place_request"  # Agregado para depuración

create_place_response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$create_place_request" $BASE_URL/)

http_code_place=$(echo "$create_place_response" | tail -n 1)
create_place_response_body=$(echo "$create_place_response" | head -n -1)

echo "Respuesta al crear el lugar con datos válidos: $create_place_response_body"  # Agregado para depuración
echo "Código de estado HTTP al crear el lugar: $http_code_place"

# Mostrar la respuesta completa en caso de error
if echo "$create_place_response_body" | jq -e '.id' &>/dev/null; then
    place_id=$(echo "$create_place_response_body" | jq -r '.id')
    echo "Lugar creado exitosamente con ID: $place_id"
else
    echo "Error al crear el lugar: $create_place_response_body"
    exit 1
fi

# Probar la función get_all_places (GET /places)
echo "Obteniendo todos los lugares..."
get_all_places_response=$(curl -s -w "%{http_code}" -X GET $BASE_URL/)
http_code_get_all=$(echo "$get_all_places_response" | tail -n 1)
get_all_response_body=$(echo "$get_all_places_response" | head -n -1)

echo "Respuesta de obtener todos los lugares: $get_all_response_body"
echo "Código de estado HTTP al obtener todos los lugares: $http_code_get_all"

if echo "$get_all_response_body" | jq -e '.[]' &>/dev/null; then
    echo "La lista de lugares se ha obtenido correctamente."
else
    echo "Error al obtener la lista de lugares: $get_all_response_body"
    exit 1
fi

# Probar la función update_place (PUT /places/{place_id})
echo "Actualizando el lugar creado con nuevo título..."
update_place_request='{
    "title": "Plaza Nueva", 
    "description": "Descripción actualizada del lugar.", 
    "price": 120.0, 
    "latitude": -34.9020, 
    "longitude": -56.1650, 
    "owner_id": "'"$owner_id"'", 
    "amenities": [
        "'"$amenity1_id"'",
        "'"$amenity2_id"'"
    ]
}'
echo "Solicitud de actualización de lugar: $update_place_request"

update_place_response=$(curl -s -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d "$update_place_request" $BASE_URL/$place_id)
http_code_update=$(echo "$update_place_response" | tail -n 1)
update_place_response_body=$(echo "$update_place_response" | head -n -1)

echo "Respuesta al actualizar el lugar: $update_place_response_body"
echo "Código de estado HTTP al actualizar el lugar: $http_code_update"

if echo "$update_place_response_body" | jq -e '.title' &>/dev/null; then
    echo "Lugar actualizado correctamente."
else
    echo "Error al actualizar el lugar: $update_place_response_body"
    exit 1
fi
