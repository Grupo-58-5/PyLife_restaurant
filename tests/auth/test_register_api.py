def test_register_api(client):
    body = {"name": "Luigi","email":"test3@gmail.com","password": "password"}
    response = client.post("/auth/sign_up",json=body)
    data = response.json()
    assert response.status_code == 201
    assert data["message"] == "Registered user"
    assert data["role"] == "CLIENT"

def test_register_repeat_email_api(client):
    body = {"name": "Luigi","email":"johnDoe@gmail.com","password": "password"}
    client.post("/auth/sign_up",json=body)

    body = {"name": "Jose","email":"johnDoe@gmail.com","password": "pass1234"}
    response = client.post("/auth/sign_up",json=body)

    assert response.status_code == 409
    data = response.json()
    assert data["detail"]['msg'] == "email already registered"

def test_register_invalid_email_api(client):
    body = {"name": "Jose","email":"string","password": "pass1234"}
    response = client.post("/auth/sign_up",json=body)

    print("JSON de respuesta:", response.json())

    assert response.status_code == 409
    data = response.json()
    assert data["detail"]['msg'] == "Wrong email format"