import pytest
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter


def test_update_profile(client):

    # Se registra un nuevo usuario
    data = {
        "name": "Dan",
        "email": "test2@gmail.com",
        "password": "Hello"
    }
    sign_up = client.post("/auth/sign_up", json=data)
    assert sign_up.status_code == 201

    # Inicia sesion para obtener el token de acceso
    form_data = {
        'username': 'test2@gmail.com',
        'password': 'Hello'
    }
    response = client.post("/auth/log_in", data=form_data)
    header_client = {"Authorization": f"Bearer {response.json().get("access_token")}"}

    # Se modifica el email del usuario registrado
    body = {
        "email": "test_update@gmail.com",
        "name": "Luigi"
    }
    update_response = client.patch("/user/change/profile",json=body,headers=header_client)
    print("respuesta: ",update_response)
    assert update_response.status_code == 200
    assert update_response.json()["email"] == "test_update@gmail.com"

def test_cannot_update_profile_with_invalid_data(client,get_token_client):

    # Se registra un nuevo usuario
    data = {
        "name": "Dan",
        "email": "test2@gmail.com",
        "password": "Hello"
    }
    sign_up = client.post("/auth/sign_up", json=data)
    assert sign_up.status_code == 201

    # Inicia sesion para obtener el token de acceso
    form_data = {
        'username': 'test2@gmail.com',
        'password': 'Hello'
    }
    response = client.post("/auth/log_in", data=form_data)
    header_client = {"Authorization": f"Bearer {response.json().get("access_token")}"}

    # Se modifica el email del usuario registrado con el mismo correo del usuario registrado en el fixture
    body = {
        "email": "test@gmail.com",
    }
    update_response = client.patch("/user/change/profile",json=body,headers=header_client)
    print("respuesta: ",update_response)
    assert update_response.status_code == 409

def test_delete_profile(client):

    # Se registra un nuevo usuario
    data = {
        "name": "Dan",
        "email": "test_delete@gmail.com",
        "password": "Hello"
    }
    sign_up = client.post("/auth/sign_up", json=data)
    assert sign_up.status_code == 201

    # Inicia sesion para obtener el token de acceso
    form_data = {
        'username': 'test_delete@gmail.com',
        'password': 'Hello'
    }
    response = client.post("/auth/log_in", data=form_data)
    assert response.status_code == 200
    header_client = {"Authorization": f"Bearer {response.json().get("access_token")}"}

    # Se elimina la cuenta del usuario actual
    delete_response = client.delete("/auth/delete/current_user", headers=header_client)
    assert delete_response.status_code == 200

    # Se verifica que la cuenta no este en el sistema
    form_data = {
        'username': 'test_delete@gmail.com',
        'password': 'Hello'
    }
    response = client.post("/auth/log_in", data=form_data)
    assert response.status_code == 403

def test_admin_can_delete_any_profile(client, get_token_admin):

    # Se registra un nuevo usuario
    data = {
        "name": "Dan",
        "email": "test_delete@gmail.com",
        "password": "Hello"
    }
    sign_up = client.post("/auth/sign_up", json=data)
    assert sign_up.status_code == 201

    # Se inicia sesion con las credenciales del usuario registrado
    form_data = {
        'username': 'test_delete@gmail.com',
        'password': 'Hello'
    }
    response = client.post("/auth/log_in", data=form_data)
    header_client = {"Authorization": f"Bearer {response.json().get("access_token")}"}

    current = client.get("/user/current_user",headers=header_client)
    print("JSON current: ",current.json())
    assert current.status_code == 200
    user_id = current.json()["id"]

    header_admin = {"Authorization": f"Bearer {get_token_admin}"}

    response_delete = client.delete(f"/auth/delete/user/{user_id}", headers=header_admin)
    print("Response: ",response_delete)
    assert response_delete.status_code == 200

def test_admin_can_get_all_users(client, get_token_admin):
    '''
    Test de Usuarios:
        ◦ Asegurar que un administrador pueda obtener todos los usuarios.
    '''
    # Se registra un nuevo usuario
    data = {
        "name": "Dan",
        "email": "test5@gmail.com",
        "password": "Hello"
    }
    sign_up = client.post("/auth/sign_up", json=data)
    assert sign_up.status_code == 201


    header_admin = {"Authorization": f"Bearer {get_token_admin}"}
    response = client.get("/user/get/users", headers=header_admin)
    print("Response: ", response)
    assert response.status_code == 200
    data = response.json()


