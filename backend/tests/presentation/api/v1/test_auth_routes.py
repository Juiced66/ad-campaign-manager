from fastapi.testclient import TestClient

# from fastapi import FastAPI
# from fastapi.routing import APIRoute
# useful to debug routes
# def test_inspect_registered_routes(test_app: FastAPI):
#     """Prints all registered routes to check if login POST exists."""
#     print("\n--- Registered Routes ---")
#     for route in test_app.routes:
#         if isinstance(route, APIRoute):
#             print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
#         # Handle APIRouter if routes are nested further (less common with include_router)
#         # elif isinstance(route, APIRouter):
#         #     print(f"Router Mounted at: {route.prefix}")
#         #     for sub_route in route.routes:
#         #          if isinstance(sub_route, APIRoute):
#         #               print(f"  Sub-Path: {sub_route.path}, Name: {sub_route.name}, Methods: {sub_route.methods}")
#     print("--- End Registered Routes ---\n")


def test_login_success(client: TestClient, create_test_user):
    email = "testlogin@example.com"
    password = "goodpassword"
    create_test_user(email=email, password=password)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, create_test_user):
    email = "wrongpass@example.com"
    password = "goodpassword"
    create_test_user(email=email, password=password)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "wrongpassword"},
    )
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_user_not_found(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nosuchuser@example.com", "password": "anypassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_invalid_payload(client: TestClient):
    # Missing password
    response = client.post("/api/v1/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422

    # Missing email
    response = client.post("/api/v1/auth/login", json={"password": "password"})
    assert response.status_code == 422

    # Invalid email format
    response = client.post(
        "/api/v1/auth/login", json={"email": "not-an-email", "password": "password"}
    )
    assert response.status_code == 422
