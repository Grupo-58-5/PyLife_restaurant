
## * TESTS for restaurants API Endpoints

## ? Verify admin can create restaurants
def test_create_restaurant(client, get_token_admin):
    '''
    Test de Restaurantes:
        ◦ Asegurar que un administrador pueda crear un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    response = client.post("/restaurants",json=body, headers=headers)
    print("JSON de respuesta:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Restaurant Calidad"
    assert data["address"] == "Caracas - Las Mercedes"
    assert data["opening_hour"] == "12:00:00"
    assert data["closing_hour"] == "22:00:00"
    assert "id" in data

## ? Verify clients must not create restaurants
def test_client_must_not_create_restaurant(client, get_token_client):
    '''
    Test de Restaurantes:
        ◦ Asegurar que un cliente no pueda crear un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_client}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    response = client.post("/restaurants",json=body, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 403

## ? Verify admin can update and delete restaurants
def test_admin_must_update_or_delete_restaurant(client, get_token_admin):
    '''
    Test de Restaurantes:
        ◦ Asegurar que un administrador pueda actualizar o eliminar un restaurante.
    '''

    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant El Test",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    response = client.post("/restaurants",json=body, headers=header_admin)
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]

    response_patch = client.patch(f"/restaurants/{restaurant_id}",json=body, headers=header_admin)
    assert response_patch.status_code == 202
    print("Respuesta update: ",response_patch)

    response_delete = client.delete(f"/restaurants/{restaurant_id}", headers=header_admin)
    print("Respuesta: ",response_delete.status_code)
    assert response_delete.status_code == 204

## ? Verify clients must not update nor delete restaurants
def test_client_must_not_update_nor_delete_restaurant(client, get_token_client, get_token_admin):
    '''
    Test de Restaurantes:
        ◦ Asegurar que un cliente no pueda actualizar un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_client}"}
    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    response = client.post("/restaurants",json=body, headers=header_admin)
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]
    response = client.patch(f"/restaurants/{restaurant_id}",json=body, headers=headers)
    print("JSON de respuesta:", response.json())
    assert response.status_code == 403
    response = client.delete(f"/restaurants/{restaurant_id}", headers=headers)
    print("JSON de respuesta:", response.json())
    assert response.status_code == 403


## ? Test for validatinf closing hour must be greater than opening hour
def test_hour_closing_create_restaurant(client, get_token_admin):
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"08:00:00"
    }
    response = client.post("/restaurants",json=body, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Closing hour must be greather than opening hour"


## ? Test for validating creating a restaurant with a table with 13 seats on restaurant creation
def test_create_restaurant_with_table_13_seats(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
        "tables":[
            {
                "table_number": 1,
                "seats": 13,
                "location": "Window",
            }
        ]
    }
    response = client.post("/restaurants",json=body, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Invalid capacity, must be between 2 and 12 seats"


## ? Test for validating creating a restaurant with a table with 1 seat on restaurant creation
def test_create_restaurant_1_seat_on_table(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
        "tables":[
            {
                "table_number": 1,
                "seats": 1,
                "location": "Window",
            }
        ]
    }
    response = client.post("/restaurants",json=body, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid capacity, must be between 2 and 12 seats"


## ? Test for validating duplicated table numbers on restaurant creation
def test_duplicated_number_restaurant_table(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que no se puedan crear dos mesas con el mismo número en un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
        "tables":[
            {
                "table_number": 1,
                "seats": 10,
                "location": "Window",
            },
            {
                "table_number": 1,
                "seats": 5,
                "location": "Window",
            },
        ]
    }
    response = client.post("/restaurants",json=body, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Table with number 1 already exists in the restaurant"


## ? Test for validating menu items with same name on restaurant creation
def test_create_restaurant_menu_items_same_name(client, get_token_admin):
    '''
    Test de Menu:
        ◦ Asegurar que no se puedan crear dos items de menú con el mismo nombre en un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
        "menu_items":[
            {
                "name": "Hamburger",
                "description": "Delicious beef burger",
                "category": "Entrada",
            },
            {
                "name": "Hamburger",
                "description": "Delicious beef burger with cheese",
                "category": "Entrada",
            },
        ]
    }
    response = client.post("/restaurants",json=body, headers=headers)

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Menu items must not repeat on a restaurant, found: hamburger"

def test_admin_can_get_all_restaurants(client, get_token_admin):
    '''
    Test de Restaurantes:
        ◦ Asegurar que un administrador pueda obtener todos los restaurantes.
    '''

    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    headers = {"Authorization": f"Bearer {get_token_admin}"}

    response = client.post("/restaurants",json=body, headers=headers)
    print("JSON de respuesta:", response.json())
    assert response.status_code == 201

    response = client.get("/restaurants", headers=headers)
    print("Response: ", response)
    assert response.status_code == 200