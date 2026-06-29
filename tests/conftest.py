import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def user_token(client):
    register = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    print("REGISTER:", register.status_code, register.json())

    login = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "Password123",
        },
    )

    print("LOGIN:", login.status_code, login.json())

    assert login.status_code == 200

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def second_user(client):
    register = client.post(
        "/auth/register",
        json={
            "username": "seconduser",
            "email": "second@example.com",
            "password": "Password123",
        },
    )

    user = register.json()

    login = client.post(
        "/auth/login",
        data={
            "username": "seconduser",
            "password": "Password123",
        },
    )

    token = login.json()["access_token"]

    return {
        "id": user["id"],
        "headers": {
            "Authorization": f"Bearer {token}"
        },
    }

@pytest.fixture
def project(client, user_token):
    response = client.post(
        "/projects/",
        headers=user_token,
        json={
            "name": "Test Project",
            "description": "Testing"
        },
    )

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def task(client, user_token, project):
    response = client.post(
        "/tasks/",
        headers=user_token,
        json={
            "project_id": project["id"],
            "title": "Test Task",
            "description": "Testing task"
        },
    )

    assert response.status_code == 201

    return response.json()