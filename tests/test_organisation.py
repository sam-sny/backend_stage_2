import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust the import as needed
from app.models import User, Organisation  # Adjust the import as needed
from app.database import SessionLocal, engine, Base  # Adjust the import as needed

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

def create_user(email: str, password: str, firstName: str, lastName: str):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "firstName": firstName,
            "lastName": lastName
            })
    assert response.status_code == 200
    return response.json()

def get_organisation_id(user_token: str):
    response = client.get("/api/organisations", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    return response.json()["data"]["organisations"][0]["orgId"]

def login_user(email: str, password: str):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        }
    )
    assert response.status_code == 200
    return response.json()["data"]["accessToken"]


def test_access_unauthorized_organisation(setup_database):
    # Create user1 and user2
    # user1 = create_user("user3@example.com", "password3", "sam", "ekpo")
    # user2 = create_user("user4@example.com", "password4", "uche", "ofia")

    # Get their JWT tokens
    user1_token = login_user("user3@example.com", "password3")
    user2_token = login_user("user4@example.com", "password4")

    # Get the organisation IDs
    user1_org_id = get_organisation_id(user1_token)
    user2_org_id = get_organisation_id(user2_token)

    # Try to access each other's organisation
    response = client.get(f"/api/organisations/{user1_org_id}", headers={"Authorization": f"Bearer {user2_token}"})
    assert response.status_code == 403

    response = client.get(f"/api/organisations/{user2_org_id}", headers={"Authorization": f"Bearer {user1_token}"})
    assert response.status_code == 403
