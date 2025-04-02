from datetime import date

from fastapi.testclient import TestClient

def test_create_campaign_success(
    client: TestClient,
    test_auth_headers: dict,
):
    """Test creating a campaign successfully when authenticated."""
    payload = {
        "name": "Authenticated Campaign",
        "description": "Successfully created campaign",
        "start_date": "2024-05-01",
        "end_date": "2024-05-31",
        "budget": 5000.50,
        "is_active": True,
    }
    response = client.post(
        "/api/v1/campaigns/", headers=test_auth_headers, json=payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["budget"] == payload["budget"]
    assert data["is_active"] == payload["is_active"]
    assert "id" in data


def test_read_campaigns_authenticated(
    client: TestClient,
    test_auth_headers: dict,
    create_test_campaign,
):
    """Test retrieving campaigns when authenticated."""
    create_test_campaign(
        name="Camp A",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        budget=100,
    )
    create_test_campaign(
        name="Camp B",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 2, 28),
        budget=200,
    )

    response = client.get("/api/v1/campaigns/", headers=test_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_specific_campaign(
    client: TestClient, test_auth_headers: dict, create_test_campaign
):
    """Test retrieving a specific campaign by ID."""
    campaign_model = create_test_campaign(
        name="Specific Camp",
        start_date=date(2024, 3, 1),
        end_date=date(2024, 3, 31),
        budget=300,
    )
    campaign_id = campaign_model.id

    response = client.get(f"/api/v1/campaigns/{campaign_id}", headers=test_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == campaign_id
    assert data["name"] == "Specific Camp"


def test_update_campaign(
    client: TestClient, test_auth_headers: dict, create_test_campaign
):
    """Test updating an existing campaign."""
    campaign_model = create_test_campaign(
        name="Update Me",
        start_date=date(2024, 4, 1),
        end_date=date(2024, 4, 30),
        budget=400,
    )
    campaign_id = campaign_model.id
    update_payload = {
        "name": "Updated Name",
        "description": "Updated description.",
        "budget": 450.75,
        "is_active": True,
    }

    response = client.put(
        f"/api/v1/campaigns/{campaign_id}",
        headers=test_auth_headers,
        json=update_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == campaign_id
    assert data["name"] == update_payload["name"]
    assert data["description"] == update_payload["description"]
    assert data["budget"] == update_payload["budget"]
    assert data["is_active"] == update_payload["is_active"]


def test_delete_campaign(
    client: TestClient, test_auth_headers: dict, create_test_campaign
):
    """Test deleting an existing campaign."""
    campaign_model = create_test_campaign(
        name="Delete Me",
        start_date=date(2024, 5, 1),
        end_date=date(2024, 5, 31),
        budget=500,
    )
    campaign_id = campaign_model.id

    # Delete the campaign
    delete_response = client.delete(
        f"/api/v1/campaigns/{campaign_id}", headers=test_auth_headers
    )
    assert delete_response.status_code == 200
    get_response = client.get(
        f"/api/v1/campaigns/{campaign_id}", headers=test_auth_headers
    )
    assert get_response.status_code == 404

def test_get_campaigns_unauthenticated(client: TestClient):
    response = client.get("/api/v1/campaigns/")
    assert response.status_code == 401
    assert (
        response.json()["detail"] == "Not authenticated"
    )


def test_create_campaign_unauthenticated(client: TestClient):
    payload = {
        "name": "Unauth Test",
        "description": "Desc",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "budget": 100.0,
        "is_active": False,
    }
    response = client.post("/api/v1/campaigns/", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_campaigns_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalid.token.string"}
    response = client.get("/api/v1/campaigns/", headers=headers)
    assert response.status_code == 401
    assert (
        response.json()["detail"] == "Could not validate credentials"
    )

def test_get_campaign_not_found(client: TestClient, test_auth_headers: dict):
    response = client.get("/api/v1/campaigns/99999", headers=test_auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Campaign not found"


def test_update_campaign_not_found(client: TestClient, test_auth_headers: dict):
    update_payload = {"name": "Nonexistent"}
    response = client.put(
        "/api/v1/campaigns/99999", headers=test_auth_headers, json=update_payload
    )
    assert response.status_code == 404
    assert (
        response.json()["detail"] == "Campaign not found"
    )


def test_delete_campaign_not_found(client: TestClient, test_auth_headers: dict):
    response = client.delete("/api/v1/campaigns/99999", headers=test_auth_headers)
    assert response.status_code == 404
    assert (
        response.json()["detail"] == "Campaign not found"
    )


def test_create_campaign_invalid_payload(client: TestClient, test_auth_headers: dict):
    invalid_payload = {"description": "Only desc"}
    response = client.post(
        "/api/v1/campaigns/", headers=test_auth_headers, json=invalid_payload
    )
    assert response.status_code == 422


def test_update_campaign_invalid_payload(
    client: TestClient, test_auth_headers: dict, create_test_campaign
):
    campaign_model = create_test_campaign(
        name="Invalid Update Target",
        start_date=date(2024, 6, 1),
        end_date=date(2024, 6, 30),
        budget=100,
    )
    campaign_id = campaign_model.id
    invalid_payload = {"budget": "not-a-number"}
    response = client.put(
        f"/api/v1/campaigns/{campaign_id}",
        headers=test_auth_headers,
        json=invalid_payload,
    )
    assert response.status_code == 422
