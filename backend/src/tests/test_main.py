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
    assert response.json() == {"detail": "Could not validate credentials"}

def test_valid_ticket_sell(client: TestClient):
    # Step 1: Register a seller
    seller = {
        "firstname": "James",
        "lastname": "Sullivan",
        "email": "james@sullivan.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=seller)
    assert response.status_code == status.HTTP_201_CREATED

    # Step 2: Log in as the seller to get a token
    data = {
        "grant_type": "password",
        "username": "james@sullivan.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # Step 3: Create a valid ticket
    ticket = {
        "name": "Concert Ticket",
        "description": "VIP Access to the concert",
        "date": "2024-12-25T19:00:00",
        "category": "Music",
        "price": 150.0
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post("/api/tickets/sell", json=ticket, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == ticket["name"]
    assert response.json()["price"] == ticket["price"]

def test_invalid_ticket_sell(client: TestClient):
    # Step 1: Register a seller
    seller = {
        "firstname": "Jozko",
        "lastname": "Mrkva",
        "email": "jozko@mrkva.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=seller)
    assert response.status_code == status.HTTP_201_CREATED

    # Step 2: Log in as the seller to get a token
    data = {
        "grant_type": "password",
        "username": "jozko@mrkva.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # Step 3: Attempt to create an invalid ticket (missing required fields)
    invalid_ticket = {
        "description": "VIP Access to the concert",  # Missing name, date, category, and price
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post("/api/tickets/sell", json=invalid_ticket, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_valid_ticket_buy(client: TestClient):
    # Step 1: Register a buyer
    buyer = {
        "firstname": "Buyer",
        "lastname": "Carrot",
        "email": "buyercarrot@mail.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=buyer)
    assert response.status_code == status.HTTP_201_CREATED
    buyer_id = response.json()["id"]

    # Step 2: Log in as the seller to get a token
    data_buyer = {
        "grant_type": "password",
        "username": "buyercarrot@mail.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data_buyer)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token_buyer = response.json()["access_token"]

    # Step 1: Register a seller
    seller = {
        "firstname": "Seller",
        "lastname": "Apple",
        "email": "sellerapple@mail.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=seller)
    assert response.status_code == status.HTTP_201_CREATED


    # Step 2: Log in as the seller to get a token
    data_seller = {
        "grant_type": "password",
        "username": "sellerapple@mail.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data_seller)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token_seller = response.json()["access_token"]

    ticket = {
        "name": "Sports Event",
        "description": "Ticket for front seats",
        "date": "2024-12-20T20:00:00",
        "category": "Sports",
        "price": 200.0
    }
    headers = {"Authorization": f"Bearer {token_seller}"}
    response = client.post("/api/tickets/sell", json=ticket, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    ticket_id = response.json()["id"]

    # Step 4: Purchase the ticket as the buyer
    purchase_request = {"id": ticket_id}
    headers = {"Authorization": f"Bearer {token_buyer}"}
    response = client.post("/api/tickets/buy", json=purchase_request, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == ticket_id
    assert response.json()["buyer_id"] == buyer_id



def test_already_purchased_ticket_buy(client: TestClient):
    # Step 1: Register a buyer
    buyer = {
        "firstname": "Buyer",
        "lastname": "Carrot",
        "email": "buyercarrot@mail.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=buyer)
    assert response.status_code == status.HTTP_201_CREATED
    buyer_id = response.json()["id"]

    # Step 2: Log in as the seller to get a token
    data_buyer = {
        "grant_type": "password",
        "username": "buyercarrot@mail.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data_buyer)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token_buyer = response.json()["access_token"]

    # Step 1: Register a seller
    seller = {
        "firstname": "Seller",
        "lastname": "Apple",
        "email": "sellerapple@mail.com",
        "password": "securepassword"
    }
    response = client.post("/api/users/register", json=seller)
    assert response.status_code == status.HTTP_201_CREATED


    # Step 2: Log in as the seller to get a token
    data_seller = {
        "grant_type": "password",
        "username": "sellerapple@mail.com",
        "password": "securepassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/api/auth/token", data=data_seller)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    token_seller = response.json()["access_token"]

    ticket = {
        "name": "Sports Event",
        "description": "Ticket for front seats",
        "date": "2024-12-20T20:00:00",
        "category": "Sports",
        "price": 200.0
    }
    headers = {"Authorization": f"Bearer {token_seller}"}
    response = client.post("/api/tickets/sell", json=ticket, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    ticket_id = response.json()["id"]

    # Step 4: Purchase the ticket as the buyer
    purchase_request = {"id": ticket_id}
    headers = {"Authorization": f"Bearer {token_buyer}"}
    response = client.post("/api/tickets/buy", json=purchase_request, headers=headers)
    # Step 5: try to purchase ticket again
    purchase_request = {"id": ticket_id}
    headers = {"Authorization": f"Bearer {token_buyer}"}
    response = client.post("/api/tickets/buy", json=purchase_request, headers=headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Ticket was already bought"



