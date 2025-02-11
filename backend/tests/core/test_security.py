from datetime import timedelta
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_jwt_token
)

def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)

def test_create_access_token():
    subject = "testuser"
    expires_delta = timedelta(minutes=20)
    token = create_access_token(subject, expires_delta)
    assert token

def test_decode_jwt_token():
    subject = "testuser"
    expires_delta = timedelta(minutes=20)
    token = create_access_token(subject, expires_delta)
    assert subject == decode_jwt_token(token)

def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)