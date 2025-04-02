from fastapi.testclient import TestClient


def test_get_user_by_id_not_found(
    client: TestClient, test_auth_headers
):
    """Test getting a user by ID that does not exist."""
    non_existent_id = 999999
    response = client.get(f"/api/v1/users/{non_existent_id}", headers=test_auth_headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_get_user_by_email_not_found(client: TestClient, test_auth_headers):
    """Test getting a user by email that does not exist."""
    non_existent_email = "nosuchuser@example.com"
    response = client.get(
        f"/api/v1/users/?email={non_existent_email}", headers=test_auth_headers
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_update_user_not_found(client: TestClient, test_auth_headers):
    """Test updating a user that does not exist."""
    non_existent_id = 999999
    update_payload = {"email": "new@example.com"}
    response = client.put(
        f"/api/v1/users/{non_existent_id}",
        json=update_payload,
        headers=test_auth_headers,
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_delete_user_not_found(client: TestClient, test_auth_headers):
    """Test deleting a user that does not exist."""
    non_existent_id = 999999
    response = client.delete(
        f"/api/v1/users/{non_existent_id}", headers=test_auth_headers
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_create_user_invalid_payload(
    client: TestClient, test_auth_headers
):
    """Test creating user with invalid payloads."""
    # Missing password
    payload_missing_pass = {"email": "test@example.com"}
    response = client.post(
        "/api/v1/users/", json=payload_missing_pass, headers=test_auth_headers
    )
    assert response.status_code == 422

    # Invalid email
    payload_invalid_email = {"email": "not-email", "password": "password123"}
    response = client.post(
        "/api/v1/users/", json=payload_invalid_email, headers=test_auth_headers
    )
    assert response.status_code == 422

    # Password too short
    payload_short_pass = {"email": "test@example.com", "password": "short"}
    response = client.post(
        "/api/v1/users/", json=payload_short_pass, headers=test_auth_headers
    )
    assert response.status_code == 422


def test_update_user_invalid_payload(
    client: TestClient, create_test_user, test_auth_headers
):
    """Test updating user with invalid payloads."""
    user = create_test_user(email="update@example.com", password="password123")

    # Invalid email format
    payload_invalid_email = {"email": "not-an-email"}
    response = client.put(
        f"/api/v1/users/{user.id}",
        json=payload_invalid_email,
        headers=test_auth_headers,
    )
    assert response.status_code == 422

    # Password too short
    payload_short_pass = {"password": "short"}
    response = client.put(
        f"/api/v1/users/{user.id}", json=payload_short_pass, headers=test_auth_headers
    )
    assert response.status_code == 422
