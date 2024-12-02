from datetime import date
import pytest

from fastapi import status
from fastapi.testclient import TestClient

from src.tests.conftest import client



def test_create_user(client: TestClient):
    user = {
        "firstname": "Mike",
        "lastname": "Wazowski",
        "email": "mike@wazowski.com",
        "password": "password"
    }
    response = client.post("/api/users/register", json=user)
    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["firstname"] == user["firstname"]
    assert response.json()["lastname"] == user["lastname"]
    assert response.json()["email"] == user["email"]


def test_create_user_incorrect_params(client: TestClient):
    user = {}
    response = client.post("/api/users/register", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

def test_get_all_users(client: TestClient):
    response = client.get("/api/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_login_user(client: TestClient):
    user = {
        "firstname": "Mike",
        "lastname": "Wazowski",
        "email": "mike@wazowski.com",
        "password": "password"
    }
    data = {
        "grant_type": "password",
        "username": "mike@wazowski.com",
        "password": "password",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/users/register", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_user(client: TestClient):
    data = {
        "grant_type": "password",
        "username": "mike@wazowski.com",
        "password": "password",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


def test_delete_user(client: TestClient):
    # Step 1: Register a user
    user = {
        "firstname": "Mike",
        "lastname": "Wazowski",
        "email": "mike@wazowski.com",
        "password": "password"
    }
    response = client.post("/api/users/register", json=user)
    assert response.status_code == status.HTTP_201_CREATED

    # Step 2: Log in to get the authentication token
    data = {
        "grant_type": "password",
        "username": "mike@wazowski.com",
        "password": "password",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # Step 3: Use the token to delete the user
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete("/api/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "User deleted successfully"


def test_delete_user_failed(client: TestClient):
    # Step 1: Register a user
    user = {
        "firstname": "Mike",
        "lastname": "Wazowski",
        "email": "mike@wazowski.com",
        "password": "password"
    }
    response = client.post("/api/users/register", json=user)
    assert response.status_code == status.HTTP_201_CREATED

    # Step 2: Attempt to delete the user without a valid token
    headers = {
        "Authorization": "Bearer invalid_token"
    }
    response = client.delete("/api/users/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate "}