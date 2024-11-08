# from fastapi.testclient import TestClient
# from app import main
# from routes.user import *
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database.models import Base

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# client = TestClient(main.app)

# def test_create_user():
#     user_data = {"name": "Dasha", "age": 88}
#     response = client.post("/user/create", json=user_data)
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["name"] == "Dasha"
#     assert response_data["age"] == 88
#     assert "id" in response_data