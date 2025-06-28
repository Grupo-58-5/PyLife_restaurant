

## * TESTS for restaurant Menu API Endpoints
## ? Test for validating menu items with same name on menu creation
def test_menu_items_same_name_for_restaurant(client):
    body_restaurant = {
        "name": "Restaurant Calidad",
        "address":"Caracas - Las Mercedes",
        "opening_hour": "12:00:00",
        "closing_hour":"22:00:00",
    }

    response = client.post("/restaurants",json=body_restaurant)
    assert response.status_code == 201
    data_restaurant = response.json()
    restaurant_id = data_restaurant["id"]
    body_menu = {
        "name": 'Hamburger Menu',
        "description": "A menu with hamburgers",
        "category": "Entrance",
    }

    response_menu_1 = client.post(f"/menu/{restaurant_id}",json=body_menu)
    print("JSON de respuesta:", response.json())
    assert response_menu_1.status_code == 201

    response_menu_2 = client.post(f"/menu/{restaurant_id}",json=body_menu)
    print("JSON de respuesta:", response.json())
    assert response_menu_2.status_code == 409
    data = response_menu_2.json()

    ##TODO Adjust when the mesj is defined
    assert data["detail"] == "Menu items must not repeat on a restaurant, found: Hamburger"


def test_client_must_not_add_menu(client):
    pass