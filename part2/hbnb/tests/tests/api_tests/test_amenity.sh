#!/bin/bash

BASE_URL="http://localhost:5000/api/v1/amenities"

# Crear un amenity
echo "Creando un nuevo amenity..."
create_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "gym"}' $BASE_URL/)
if echo "$create_response" | jq -e '.id' &>/dev/null; then
    amenity_id=$(echo "$create_response" | jq -r '.id')
    echo "Amenity creado exitosamente: $create_response"
else
    echo "Error al crear el amenity: $create_response"
    exit 1
fi

# Obtener todos los amenities después de crear uno
echo "Obteniendo todos los amenities..."
get_all_response=$(curl -s -X GET $BASE_URL/)
echo "Estado actual de amenities: $get_all_response"

# Obtener amenity por ID
echo "Obteniendo amenity con ID: $amenity_id..."
get_response=$(curl -s -X GET $BASE_URL/$amenity_id)
if echo "$get_response" | jq -e '.name' &>/dev/null; then
    echo "Amenity obtenido correctamente: $get_response"
else
    echo "Error al obtener amenity: $get_response"
    exit 1
fi

# Actualizar un amenity
echo "Actualizando amenity con ID: $amenity_id..."
update_response=$(curl -s -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Gym"}' $BASE_URL/$amenity_id)
if echo "$update_response" | jq -e '.name' | grep -q "Updated Gym"; then
    echo "Amenity actualizado correctamente: $update_response"
else
   echo "Error al actualizar amenity: $update_response"
   exit 1
fi

# Preguntar si quieres borrar todos los amenities
echo "¿Deseas borrar todos los amenities? (s/n)"
read -p "Escribe 's' para borrar o 'n' para no borrar: " borrar

if [[ "$borrar" == "s" ]]; then
    # Obtener todos los amenities para eliminar
    echo "Obteniendo todos los amenities para eliminar..."
    get_all_response=$(curl -s -X GET $BASE_URL/)
    amenities_ids=$(echo "$get_all_response" | jq -r '.[].id')

    # Verificar si se obtuvieron amenities
    if [ -z "$amenities_ids" ]; then
        echo "No hay amenities para borrar."
    else
        # Borrar cada amenity
        echo "Borrando todos los amenities..."
        for amenity_id in $amenities_ids; do
            delete_response=$(curl -s -X DELETE $BASE_URL/$amenity_id)
            if echo "$delete_response" | grep -q "success"; then
                echo "Amenity con ID $amenity_id borrado exitosamente."
            else
                echo "Error al borrar amenity con ID $amenity_id: $delete_response"
            fi
        done

        # Verificar que los amenities fueron borrados
        echo "Verificando que los amenities fueron borrados..."
        get_all_response_after=$(curl -s -X GET $BASE_URL/)
        if [ "$(echo "$get_all_response_after" | jq '. | length')" -eq 0 ]; then
            echo "Todos los amenities han sido borrados exitosamente."
        else
            echo "Aún quedan amenities: $get_all_response_after"
        fi
    fi
else
    echo "No se han borrado los amenities."
fi
