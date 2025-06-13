

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
