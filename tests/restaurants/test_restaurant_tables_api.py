

## * TESTS for Restaurant Tables API Endpoints

## ? Test for validating creating a table with 13 seats on table creation
def test_create_restaurant_table_13_seats(client,prepare_db):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
    body_restaurant = {
        "name": "Restaurant - table 13 seats",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response = client.post("/restaurants",json=body_restaurant)
    print("JSON de respuesta:", response.json())
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]

    body_table = {
        "table_number": 1,
        "seats": 13,
        "location": "Window",
    }
    response = client.post(f"/tables/{restaurant_id}",json=body_table)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table must have between 2 and 12 seats, not 13"


## ? Test for validating creating a table with 1 seat on table creation
def test_create_table_restaurant_1_seat(client,prepare_db):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
    body_restaurant = {
        "name": "Restaurant - table 1 seat",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response = client.post("/restaurants",json=body_restaurant)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]

    body_table = {
        "table_number": 1,
        "seats": 1,
        "location": "Window",
    }
    response = client.post(f"/tables/{restaurant_id}",json=body_table)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table must have between 2 and 12 seats"


## ? Test for validating duplicated table numbers for a restaurant on table creation
def test_duplicated_number_table_for_restaurant(client,prepare_db):
    body_restaurant = {
        "name": "Restaurant - table number duplicated",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00"
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant)

    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]

    body_table = {
        "table_number": 1,
        "seats": 10,
        "location": "Window",
    }
    response_table_1 = client.post(f"/tables/{restaurant_id}",json=body_table)

    assert response_table_1.status_code == 201

    response_table_2 = client.post(f"/tables/{restaurant_id}",json=body_table)

    assert response_table_2.status_code == 409
    data = response_table_2.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table numbers must not repeat on a restaurant"
