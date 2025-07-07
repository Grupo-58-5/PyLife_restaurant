def test_cancel_reservation_by_client(client, get_token_client, get_token_admin,insert_restaurant):
    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    reserv_data = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data, headers=header_client)
    assert response_reservation.status_code == 201
    reservation_id = response_reservation.json()["reservation_id"]

    param = {"reservation_id": reservation_id}
    response_cancel = client.patch("/reservation/cancel", params=param, headers=header_client)
    assert response_cancel.status_code == 200


def test_invalid_change_state(client, get_token_client, get_token_admin,insert_restaurant):
    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    # Crea la reservacion
    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-29T17:58:53.323Z",
        "finish_time": "2025-07-29T19:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    reservation_id = response_reservation.json()["reservation_id"]
    assert response_reservation.status_code == 201

    # Modifica el estado de la reservacion a cancelada
    params = {
        "reservation_id ": reservation_id,
        "status": "canceled"
    }
    response = client.patch(f"/reservation/admin/change_status/{reservation_id}/", params=params, headers=header_admin)
    assert response.status_code == 202

    # Intenta cambiarlo a compleada, pero por el estado actual debe fallar
    params = {
        "reservation_id ": reservation_id,
        "status": "completed"
    }
    response = client.patch(f"/reservation/admin/change_status/{reservation_id}/", params=params, headers=header_client)
    assert response.status_code == 403

def test_client_cannot_change_state(client, get_token_client, get_token_admin,insert_restaurant):
    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    reservation_id = response_reservation.json()["reservation_id"]
    assert response_reservation.status_code == 201

    params = {
        "reservation_id ": reservation_id,
        "status": "canceled"
    }
    response = client.patch(f"/reservation/admin/change_status/{reservation_id}/", params=params, headers=header_admin)
    assert response.status_code == 202

    params = {
        "reservation_id ": reservation_id,
        "status": "confirmed"
    }
    response = client.patch(f"/reservation/admin/change_status/{reservation_id}/", params=params, headers=header_admin)
    assert response.status_code == 400

def test_cannot_create_reservations_with_invalid_data(client, get_token_admin, get_token_client, insert_restaurant):
    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    # Valida que no se pueda crear si la hora de inicio es mayor a la hora de cierre
    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T15:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    assert response_reservation.status_code == 400

    # Valida que no se pueda crear si dura mas de 4 horas
    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-26T10:58:53.323Z",
        "finish_time": "2025-07-26T15:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    assert response_reservation.status_code == 400

    # Valida que no se puedan preeordenar mas de 5 platos en la reservacion
    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "dishes": [
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        ],
        "start_time": "2025-07-26T10:58:53.323Z",
        "finish_time": "2025-07-26T15:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    assert response_reservation.status_code == 400

def test_cannot_create_overlapping_reservations(client, get_token_admin, get_token_client, insert_restaurant):

    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    body_menu = {
        "name": 'Hamburger Menu',
        "description": "A menu with hamburgers",
        "category": "Entrada",
    }
    response_menu = client.post(f"/menu/{restaurant_id}", json=body_menu, headers=header_admin)
    assert response_menu.status_code == 201
    menu_id = response_menu.json()["item"]["id"]

    # Crea la primera reserva exitosamente
    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "dishes": [
            f"{menu_id}"
        ],
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }

    response_1 = client.post("/reservation/", json=reserv_data_1, headers=header_client)
    assert response_1.status_code == 201

    # Define los datos de la segunda reserva que se superpone con la primera
    reserv_data_2 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "dishes": [
            f"{menu_id}"
        ],
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }

    # Intenta crear la segunda reserva y verifica que falle
    response_2 = client.post("/reservation/", json=reserv_data_2, headers=header_client)
    assert response_2.status_code == 409

def test_cannot_create_reservation_with_invalid_dish(client, get_token_client, insert_restaurant):

    header_client = {"Authorization": f"Bearer {get_token_client}"}
    restaurant_id = insert_restaurant[0]
    table_id = insert_restaurant[1]

    # Datos de la reserva usando el UUID de un plato no existente
    reserv_data_2 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "dishes": [
            "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        ],
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }
    response = client.post("/reservation/", json=reserv_data_2, headers=header_client)
    assert response.status_code == 400
    assert response.json()["detail"]["msg"] == "Dish #3fa85f64-5717-4562-b3fc-2c963f66afa6 does not belong to the restaurant menu"


def test_cannot_cancel_reservation_from_other_client(client, get_token_client, get_token_admin,insert_restaurant):
    header_client_1 = {"Authorization": f"Bearer {get_token_client}"}
    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    restaurant_id = insert_restaurant[0]

    body_table = {
        "table_number": 10,
        "seats": 10,
        "location": "Indoor"
    }

    response_table = client.post(f"/table/{restaurant_id}",json=body_table, headers=header_admin)
    table_id = response_table.json()["id"]

    data = {
        "name": "Harry",
        "email": "kal@gmail.com",
        "password": "string"
    }
    response = client.post("/auth/sign_up", json=data)

    form_data = {
        'username': 'kal@gmail.com',
        'password': 'string'
    }
    response = client.post("/auth/log_in", data=form_data)
    header_client_2 = {"Authorization": f"Bearer {response.json().get("access_token")}"}

    reserv_data_1 = {
        "restaurant_id": f"{restaurant_id}",
        "table_id": f"{table_id}",
        "start_time": "2025-07-26T17:58:53.323Z",
        "finish_time": "2025-07-26T19:58:53.323Z"
    }

    response_reservation = client.post("/reservation/", json=reserv_data_1, headers=header_client_1)
    assert response_reservation.status_code == 201
    reservation_id = response_reservation.json()["reservation_id"]

    param = {"reservation_id": reservation_id}
    response_cancel = client.patch("/reservation/cancel", params=param, headers=header_client_2)
    assert response_cancel.status_code == 403