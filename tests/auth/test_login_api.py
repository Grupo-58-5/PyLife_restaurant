def test_login_api(client):
    user = {"name": "Luigi","email":"johnDoe@gmail.com","password": "password"}
    client.post("/auth/sign_up",json=user)

    # Define los datos del formulario
    form_data = {
        'username': 'johnDoe@gmail.com',
        'password': 'password'
    }

    response = client.post("/auth/log_in",data=form_data)
    print("Login response: ",response.json())
    assert response.status_code == 200

def test_login_invalid_email_api(client):
    user = {"name": "Luigi","email":"johnDoe@gmail.com","password": "password"}
    client.post("/auth/sign_up",json=user)

    form_data = {
        'username': 'kaladin@gmail.com',
        'password': 'password'
    }
    response = client.post("/auth/log_in",data=form_data)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Wrong email"

def test_login_invalid_password_api(client):
    user = {"name": "Luigi","email":"johnDoe@gmail.com","password": "password"}
    client.post("/auth/sign_up",json=user)

    # Define los datos del formulario
    form_data = {
        'username': 'johnDoe@gmail.com',
        'password': 'pass123'
    }

    response = client.post("/auth/log_in",data=form_data)
    assert response.status_code == 403
    data = response.json()
    print("Data del response: ",data)
    assert data["detail"] == "Wrong password"