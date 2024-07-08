import pytest
import httpx

BASE_URL = "http://localhost:8000/api"

@pytest.mark.asyncio
async def test_create_organisation_success():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/organisations", json={
            "name": "Test Organisation",
            "description": "A test organisation"
        })
        assert response.status_code == 201
        json_response = response.json()
        assert json_response["status"] == "success"
        assert json_response["data"]["name"] == "Test Organisation"

@pytest.mark.asyncio
async def test_add_user_to_organisation():
    async with httpx.AsyncClient() as client:
        org_response = await client.post(f"{BASE_URL}/organisations", json={
            "name": "Test Organisation",
            "description": "A test organisation"
        })
        org_id = org_response.json()["data"]["orgId"]

        user_response = await client.post(f"{BASE_URL}/auth/register", json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane.doe@example.com",
            "password": "securepassword"
        })
        user_id = user_response.json()["data"]["user"]["userId"]

        response = await client.post(f"{BASE_URL}/organisations/{org_id}/users", json={
            "userId": user_id
        })
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == "success"
