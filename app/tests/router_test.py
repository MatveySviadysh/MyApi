from fastapi.testclient import TestClient
from main import app
from routes.items import * 
from routes.user import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Post
from utils.helpers import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    user_data = {"name": "Dasha", "age": 88}
    
    response = client.post("/user/create", json=user_data)
    
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data["name"] == "Dasha"
    assert response_data["age"] == 88
    assert "id" in response_data

def test_create_post():
    post_data = {"title": "Test Post", "text": "This is a test post", "author_id": 1}
    
    response = client.post("/post/create", json=post_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Post"
    assert response_data["text"] == "This is a test post"
    assert response_data["author_id"] == 1

def test_get_all_posts():
    response = client.get("/post/all")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    if response_data:
        assert "title" in response_data[0]

def test_delete_post():
    post_data = {"title": "Delete Me", "text": "To be deleted", "author_id": 1}
    post_response = client.post("/post/create", json=post_data)
    post_id = post_response.json()["id"]
    
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Post deleted successfully"}


# def test_update_post():
#     post_data = {"title": "Update Me", "text": "Before update", "author_id": 1}
#     post_response = client.post("/post/create", json=post_data)
#     post_id = post_response.json()["id"]
    
#     updated_data = {"title": "Updated Title", "text": "After update"}
    
#     response = client.put(f"/post/{post_id}", json=updated_data)
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["title"] == "Updated Title"
#     assert response_data["text"] == "After update"

