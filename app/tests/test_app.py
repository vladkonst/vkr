import pytest
from main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import get_db

#client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_gen():
    with TestClient(app) as client:
        response = client.post("/generate-token", data={
            'UUID': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'phone_number' : '79196943405'
        })
        assert response.status_code == 200
        assert response.json()['message'] == 'success'

def test_valid():
    with TestClient(app) as client:
        response = client .post("/generate-token", data={
            'UUID': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'phone_number' : '79196943405'
        })
        otp = response.json()['call_details']['pin']
        response = client .post("/validate-token", data={
            'UUID': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'otp' : f'{otp}'
        })
        assert response.status_code == 200
        assert response.json()['message'] == 'validated'
