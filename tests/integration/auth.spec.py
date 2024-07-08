import pytest
import httpx

BASE_URL = "http://localhost:8000/api"

@pytest.mark.asyncio
async def test_register_user_success():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/auth/register", json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        })
        assert response.status_code == 201
        json_response = response.json()
        assert json_response["status"] == "success"
        assert json_response["data"]["user"]["email"] == "john.doe@example.com"
        assert "token" in json_response["data"]

@pytest.mark.asyncio
async def test_register_missing_fields():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/auth/register", json={
            "firstName": "John",
            "lastName": "Doe",
            "password": "securepassword"
        })
        assert response.status_code == 422

        response = await client.post(f"{BASE_URL}/auth/register", json={
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/auth/register", json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        })
        response = await client.post(f"{BASE_URL}/auth/register", json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "anotherpassword"
        })
        assert response.status_code == 422
