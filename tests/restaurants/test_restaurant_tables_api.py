

## * TESTS for Restaurant Tables API Endpoints

## ? Test validate creation of a table
def test_create_table(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que un administrador pueda crear una mesa.
    '''
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test table",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    body_table = {
        "table_number": 10,
        "seats": 10,
        "location": "Indoor"
    }

    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers_admin)
    print("JSON de respuesta:", response_table.json())
    assert response_table.status_code == 201

## ? Test validate change of a table
def test_change_and_delete_table(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que un administrador pueda modificar y eliminar una mesa.
    '''
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test table",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    body_table = {
        "table_number": 10,
        "seats": 5,
        "location": "Indoor"
    }

    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers_admin)
    print("JSON de respuesta:", response_table.json())
    assert response_table.status_code == 201
    table_id = response_table.json()["id"]

    body = {
        "table_number": 4,
        "seats": 10,
        "location": "Window"
    }
    response_change = client.put(f"/table/{restaurant_id}/{table_id}",json=body, headers=headers_admin)
    print("JSON de respuesta:", response_change.json())
    assert response_change.status_code == 202
    assert response_change.json()["seats"] == 10

    response_table_delete = client.delete(f"/table/{restaurant_id}/{4}", headers=headers_admin)
    print("status code:", response_table_delete.status_code)
    assert response_table_delete.status_code == 204

def test_admin_must_get_all_tables(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que un administrador pueda obtener todas las mesas de un restaurante.
    '''
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test table",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    
    body_table = {
        "table_number": 10,
        "seats": 10,
        "location": "Indoor"
    }

    response_create = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers_admin)
    assert response_create.status_code == 201

    params = {
        "restaurant_id": restaurant_id,
        "capacity": 10
    }

    response_tables = client.get(f"/table/{restaurant_id}", params=params,headers=headers_admin)
    print("JSON de respuesta:", response_tables.json())
    assert response_tables.status_code == 200
    assert len(response_tables.json()["tables"]) > 0


## ? Test validate clients must not create tables
def test_client_must_not_create_table(client, get_token_admin ,get_token_client):
    '''
    Test de Mesas:
        ◦ Asegurar que un cliente no pueda crear una mesa.
    '''
    headers_client = {"Authorization": f"Bearer {get_token_client}"}
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test table",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    body_table = {
        "table_number": 10,
        "seats": 13,
        "location": "Indoor"
    }

    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers_client)
    print("JSON de respuesta:", response_table.json())
    assert response_table.status_code == 403


## ? Test validate clients must not update or delete tables
def test_client_must_not_update_nor_delete_table(client, get_token_admin, get_token_client):
    '''
    Test de Mesas:
        ◦ Asegurar que un cliente no pueda actualizar una mesa.
    '''
    headers_client = {"Authorization": f"Bearer {get_token_client}"}
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test table",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    body_table = {
        "table_number": 10,
        "seats": 7,
        "location": "Indoor"
    }   
    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers_admin)
    print("Response: ",response_table)
    print("JSON: ",response_table.json())
    assert response_table.status_code == 201
    data_table = response_table.json()
    table_id = data_table["id"] ## ! Or number table depends on the implementation
    body_table_update = {
        "table_number": 10,
        "seats": 10,
        "location": "Outdoor"
    }
    response_table_update = client.put(f"/table/{restaurant_id}/{table_id}",json=body_table_update, headers=headers_client)
    response_table_update_json = response_table_update.json()
    print("JSON de respuesta:", response_table_update_json)
    assert response_table_update.status_code == 403

    response_table_delete = client.delete(f"/table/{restaurant_id}/{table_id}", headers=headers_client)
    print("JSON de respuesta:", response_table_delete.json())
    assert response_table_delete.status_code == 403



## ? Test for validating creating a table with 13 seats on table creation
def test_create_restaurant_table_13_seats(client, get_token_admin):
    body_restaurant = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }

    headers = {"Authorization": f"Bearer {get_token_admin}"}

    response = client.post("/restaurants", json=body_restaurant, headers=headers)
    assert response.status_code == 201
    data_restaurant = response.json()
    restaurant_id = data_restaurant["id"]
    body_table = {
        "table_number": 10,
        "seats": 13,
        "location": "Indoor"
    }

    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers)
    print("JSON de respuesta:", response.json())
    assert response_table.status_code == 400
    data = response_table.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Invalid capacity, must be between 2 and 12 seats"




## ? Test for validating creating a table with 1 seat on table creation
def test_create_table_restaurant_1_seat(client, get_token_admin):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}

    body_restaurant = {
        "name": "Restaurant - table 1 seat",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }

    response = client.post("/restaurants",json=body_restaurant, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]

    body_table = {
        "table_number": 1,
        "seats": 1,
        "location": "Window",
    }
    response = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Invalid capacity, must be between 2 and 12 seats"


## ? Test for validating duplicated table numbers for a restaurant on table creation
def test_duplicated_number_table_for_restaurant(client, get_token_admin):

    '''
    Test de Mesas:
        ◦ Asegurar que no se pueda crear una mesa con un número de mesa ya existente en el restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}

    body_restaurant = {
        "name": "Restaurant - table name",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }

    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers)

    assert response_restaurant.status_code == 201

    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]

    body_table = {
        "table_number": 1,
        "seats": 10,
        "location": "Window",
    }
    response_table_1 = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers)

    assert response_table_1.status_code == 201

    response_table_2 = client.post(f"/table/{restaurant_id}",json=body_table, headers=headers)

    assert response_table_2.status_code == 409
    data = response_table_2.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Table with number 1 already exists in the restaurant"
