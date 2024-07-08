import pytest
from datetime import timedelta
from app.auth import create_access_token, decode_access_token

def test_token_expiry():
    token = create_access_token(data={"sub": "test_user"}, expires_delta=timedelta(minutes=1))
    decoded_token = decode_access_token(token)
    assert decoded_token is None

def test_token_user_details():
    token = create_access_token(data={"email": "test@example.com"})
    decoded_token = decode_access_token(token)
    assert decoded_token is not None
    assert decoded_token.email == "test@example.com"


