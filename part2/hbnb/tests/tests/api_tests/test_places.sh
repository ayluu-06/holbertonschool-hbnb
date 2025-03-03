#!/bin/bash

BASE_URL="http://localhost:5000/api/v1/places"
BASE_URL_USERS="http://localhost:5000/api/v1/users"
BASE_URL_AMENITIES="http://localhost:5000/api/v1/amenities"

# Crear un nuevo usuario (owner) si no existe
echo "Creando un nuevo usuario..."
create_user_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email": "asassaasda@example.com", "first_name": "Juan", "last_name": "Pérez"}' $BASE_URL_USERS/)
echo "Respuesta de crear usuario: $create_user_response"  # Agregado para depuración

if echo "$create_user_response" | jq -e '.id' &>/dev/null; then
    owner_id=$(echo "$create_user_response" | jq -r '.id')
    echo "Usuario creado exitosamente con ID: $owner_id"
else
    echo "Error al crear el usuario: $create_user_response"
    exit 1
fi

# Crear amenities si no existen
echo "Creando amenities..."
create_amenity1_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "amenity1"}' $BASE_URL_AMENITIES/)
create_amenity2_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "amenity2"}' $BASE_URL_AMENITIES/)

amenity1_id=$(echo "$create_amenity1_response" | jq -r '.id')
amenity2_id=$(echo "$create_amenity2_response" | jq -r '.id')

echo "Amenity1 creado con ID: $amenity1_id"
echo "Amenity2 creado con ID: $amenity2_id"

# Crear un lugar (place) con los campos adicionales requeridos
echo "Creando un nuevo lugar..."
create_place_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "title": "Plaza Principal", 
    "description": "Este es un lugar icónico en el centro de Montevideo.", 
    "price": 100.0, 
    "latitude": -34.9011, 
    "longitude": -56.1645, 
    "owner_id": "'"$owner_id"'", 
    "amenities": [
        "'"$amenity1_id"'",
        "'"$amenity2_id"'"
    ]
}' $BASE_URL/)

if echo "$create_place_response" | jq -e '.id' &>/dev/null; then
    place_id=$(echo "$create_place_response" | jq -r '.id')
    echo "Lugar creado exitosamente con ID: $place_id"
else
    echo "Error al crear el lugar: $create_place_response"
    exit 1
fi

# Obtener todos los lugares después de crear uno
echo "Obteniendo todos los lugares..."
get_all_response=$(curl -s -X GET $BASE_URL/)
echo "Estado actual de lugares: $get_all_response"

# Obtener lugar por ID
echo "Obteniendo lugar con ID: $place_id..."
get_response=$(curl -s -X GET $BASE_URL/$place_id)
if echo "$get_response" | jq -e '.title' &>/dev/null; then
    echo "Lugar obtenido correctamente: $get_response"
else
    echo "Error al obtener lugar: $get_response"
    exit 1
fi

# Actualizar un lugar
echo "Actualizando lugar con ID: $place_id..."
update_response=$(curl -s -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Plaza Mayor", "description": "Updated description", "price": 120.0, "latitude": -34.9020, "longitude": -56.1650}' $BASE_URL/$place_id)
if echo "$update_response" | jq -e '.title' | grep -q "Updated Plaza Mayor"; then
    echo "Lugar actualizado correctamente: $update_response"
else
    echo "Error al actualizar lugar: $update_response"
    exit 1
fi

# Preguntar si quieres borrar todos los lugares
echo "¿Deseas borrar todos los lugares? (s/n)"
read -p "Escribe 's' para borrar o 'n' para no borrar: " borrar

if [[ "$borrar" == "s" ]]; then
    # Obtener todos los lugares para eliminar
    echo "Obteniendo todos los lugares para eliminar..."
    get_all_response=$(curl -s -X GET $BASE_URL/)
    places_ids=$(echo "$get_all_response" | jq -r '.[].id')

    # Verificar si se obtuvieron lugares
    if [ -z "$places_ids" ]; then
        echo "No hay lugares para borrar."
    else
        # Borrar cada lugar
        echo "Borrando todos los lugares..."
        for place_id in $places_ids; do
            delete_response=$(curl -s -X DELETE $BASE_URL/$place_id)
            if echo "$delete_response" | jq -e '.message' | grep -q "success"; then
                echo "Lugar con ID $place_id borrado exitosamente."
            else
                echo "Error al borrar lugar con ID $place_id: $delete_response"
            fi
        done

        # Verificar que los lugares fueron borrados
        echo "Verificando que los lugares fueron borrados..."
        get_all_response_after=$(curl -s -X GET $BASE_URL/)
        if [ "$(echo "$get_all_response_after" | jq '. | length')" -eq 0 ]; then
            echo "Todos los lugares han sido borrados exitosamente."
        else
            echo "Aún quedan lugares: $get_all_response_after"
        fi
    fi
else
    echo "No se han borrado los lugares."
fi
