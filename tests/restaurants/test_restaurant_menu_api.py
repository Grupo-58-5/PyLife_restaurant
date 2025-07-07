

## * TESTS for restaurant Menu API Endpoints
## ? Test for validating menu items with same name on menu creation
def test_menu_items_same_name_for_restaurant(client, get_token_admin):
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
    body_menu = {
        "name": 'Hamburger Menu',
        "description": "A menu with hamburgers",
        "category": "Principal",
    }

    response_menu_1 = client.post(f"/menu/{restaurant_id}",json=body_menu, headers=headers)
    print("Response: ",response_menu_1)
    print("JSON de respuesta:", response_menu_1.json())
    assert response_menu_1.status_code == 201

    response_menu_2 = client.post(f"/menu/{restaurant_id}",json=body_menu, headers=headers)
    print("JSON de respuesta:", response.json())
    assert response_menu_2.status_code == 409
    data = response_menu_2.json()

    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Menu items must not repeat on a restaurant, found: hamburger menu"


def test_menu_item_of_another_restaurant_on_reservation_creation(client, get_token_client, get_token_admin, insert_restaurant):

    # Obtener los header y UUID's a traves del fixture
    headers_client = {"Authorization": f"Bearer {get_token_client}"}
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    # Crear un segundo restaurante
    body_restaurant = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }

    response = client.post("/restaurants", json=body_restaurant, headers=headers_admin)
    data_restaurant = response.json()
    restaurant2_id = data_restaurant["id"]

    # Asignar un menu al segundo restaurante creado
    body_menu = {
        "name": 'Hamburger Menu',
        "description": "A menu with hamburgers",
        "category": "Entrada",
    }

    response_menu = client.post(f"/menu/{restaurant2_id}",json=body_menu, headers=headers_admin)
    print("JSON de respuesta:", response_menu.json())
    menu_id = response_menu.json()["item"]["id"]

    # Crear una reservacion para el restaurante creado por el fixture pero con menu del segundo restaurante
    body_reservation = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{str(table_id)}",
        "dishes": [
            f"{str(menu_id)}"
        ],
        "start_time": "2025-08-05T12:30:27.535Z",
        "finish_time": "2025-08-05T15:30:27.535Z"
    }
    response_reservation = client.post(f"/reservation/",json=body_reservation, headers=headers_client)
    assert response_reservation.status_code == 400

def test_client_must_not_add_menu(client, get_token_client, get_token_admin):
    '''
    Test de Menú:
        ◦ Asegurar que un cliente no pueda agregar un menú a un restaurante.
    '''
    headers = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",  
    }
    response = client.post("/restaurants", json=body_restaurant, headers=headers)
    assert response.status_code == 201
    data_restaurant = response.json()
    restaurant_id = data_restaurant["id"]
    body_menu = {
        "name": 'Hamburger Menu',
        "description": "A menu with hamburgers",
        "category": "Entrada",
    }
    headers_client = {"Authorization": f"Bearer {get_token_client}"}
    response_menu = client.post(f"/menu/{restaurant_id}", json=body_menu, headers=headers_client)
    assert response_menu.status_code == 403

def test_client_must_not_update_nor_delete_menu(client, get_token_client, get_token_admin):
    '''
    Test de Menú:
        ◦ Asegurar que un cliente no pueda actualizar ni eliminar un menú de un restaurante.
    '''
    headers_client = {"Authorization": f"Bearer {get_token_client}"}
    headers_admin = {"Authorization": f"Bearer {get_token_admin}"}
    body_restaurant = {
        "name": "client test menu",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }
    response_restaurant = client.post("/restaurants",json=body_restaurant, headers=headers_admin)
    assert response_restaurant.status_code == 201
    data_restaurant = response_restaurant.json()
    restaurant_id = data_restaurant["id"]
    body_menu = {
        "name": "Menu Test",
        "description": "Test Menu Description",
        "category": "Entrada"
    }
    response_menu = client.post(f"/menu/{restaurant_id}",json=body_menu, headers=headers_admin)
    assert response_menu.status_code == 201
    data_menu = response_menu.json()
    menu_id = data_menu["item"]["id"] # Assuming the response contains the menu ID
    body_menu_update = {
        "name": "Updated Menu",
        "description": "Updated Description",
        "category": "Main Course"
    }
    response_menu_update = client.put(f"/menu/{restaurant_id}/menu/{menu_id}",json=body_menu_update, headers=headers_client)
    response_menu_update_json = response_menu_update.json()
    print("JSON de respuesta:", response_menu_update_json)
    assert response_menu_update.status_code == 403

    param = {"menu_id": menu_id}

    response_menu_delete = client.delete(f"/menu/{restaurant_id}", params=param,headers=headers_client)
    print("JSON de respuesta:", response_menu_delete.json())
    assert response_menu_delete.status_code == 403
