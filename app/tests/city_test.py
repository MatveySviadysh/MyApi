# import pytest
# from fastapi.testclient import TestClient
# from fastapi import FastAPI
# from routes.user import user_router
# from routes.city import city_router
# app = FastAPI()

# app.include_router(user_router)
# app.include_router(city_router)
# client = TestClient(app)

# @pytest.fixture
# def create_city():
#     city_data = {"name": "Test City", "description": "A test city", "image_url": "http://test.com/image.png"}
#     response = client.post("/city/create", json=city_data)
#     return response.json()

# def test_create_city():
#     city_data = {"name": "New City", "description": "A new city", "image_url": "http://example.com/image.png"}
#     response = client.post("/city/create", json=city_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == city_data["name"]

# def test_create_duplicate_city(create_city):
#     duplicate_city_data = {"name": "Test City", "description": "A duplicate city", "image_url": "http://duplicate.com/image.png"}
#     response = client.post("/city/create", json=duplicate_city_data)
#     assert response.status_code == 400
#     assert response.json()["detail"] == "City with this name already exists."

# def test_get_cities():
#     response = client.get("/cities")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_get_city(create_city):
#     response = client.get("/city", params={"id": create_city["id"]})
#     assert response.status_code == 200
#     assert response.json()["name"] == create_city["name"]

# def test_update_city(create_city):
#     updated_data = {"name": "Updated City", "description": "An updated city", "image_url": "http://example.com/updated.png"}
#     response = client.put(f"/city/{create_city['id']}", json=updated_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == updated_data["name"]

# def test_delete_city(create_city):
#     response = client.delete(f"/city/{create_city['id']}")
#     assert response.status_code == 200
#     assert response.json()["message"] == "City deleted successfully"
