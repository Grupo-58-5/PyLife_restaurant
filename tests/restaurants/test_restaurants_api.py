
## * TESTS for restaurants API Endpoints

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
    assert data["detail"] == "Invalid capacity, must be between 2 and 12"


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
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Invalid capacity, must be between 2 and 12"


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
    ##TODO Adjust when the mesj is defined
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
                "category": "Entrance",
            },
            {
                "name": "Hamburger",
                "description": "Delicious beef burger with cheese",
                "category": "Entrance",
            },
        ]
    }
    response = client.post("/restaurants",json=body, headers=headers)

    assert response.status_code == 409
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Menu items must not repeat on a restaurant, found: hamburger"
