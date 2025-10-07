import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.db.models import Base, User, Order
from app.core.security import hash_password

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_user(setup_database):
    db = TestingSessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            return existing_admin
            
        user = User(
            username="admin",
            email="admin@test.com",
            hashed_password=hash_password("Admin123"),
            role="admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@pytest.fixture
def regular_user(setup_database):
    db = TestingSessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "user1").first()
        if existing_user:
            return existing_user
            
        user = User(
            username="user1",
            email="user1@test.com",
            hashed_password=hash_password("User123"),
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@pytest.fixture
def admin_token(client, admin_user):
    response = client.post("/auth/login", json={"username": "admin", "password": "Admin123"})
    return response.json()["access_token"]

@pytest.fixture
def user_token(client, regular_user):
    response = client.post("/auth/login", json={"username": "user1", "password": "User123"})
    return response.json()["access_token"]
