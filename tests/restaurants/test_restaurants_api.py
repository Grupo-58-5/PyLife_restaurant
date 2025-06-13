

def test_hour_closing_create_restaurant(client,prepare_db):
    body = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"08:00:00"
    }
    response = client.post("/restaurants",json=body)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]['msg'] == "Closing hour must be greather than opening hour"

def test_hour_closing_create_restaurant_13_seats(client,prepare_db):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
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
    response = client.post("/restaurants",json=body)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table must have between 2 and 12 seats, not 13"

def test_hour_closing_create_restaurant_1_seat(client,prepare_db):
    '''
    Test de Mesas:
        ◦ Asegurar que una mesa con capacidad 1 o 13 sea rechazada.
    '''
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
    response = client.post("/restaurants",json=body)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 400
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table must have between 2 and 12 seats, not 1"


def test_duplicated_number_table(client,prepare_db):
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
    response = client.post("/restaurants",json=body)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 409
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Table numbers must not repeat on a restaurant"


def test_menu_items_same_name(client,prepare_db):
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
    response = client.post("/restaurants",json=body)
    print("JSON de respuesta:", response.json())

    assert response.status_code == 409
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Menu items must not repeat on a restaurant, found: Hamburger"

def test_menu_items_same_name(client,prepare_db):
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
    response = client.post("/restaurants",json=body)
    print("JSON de respuesta:", response.json())

    assert response.status_code == 409
    data = response.json()
    ##TODO Adjust when the mesj is defined
    assert data["detail"]['msg'] == "Menu items must not repeat on a restaurant, found: Hamburger"

def test_client_must_not_add_menu(client, prepare_db):
    pass