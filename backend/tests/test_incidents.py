def test_create_incident(client, auth_headers):
    response = client.post(
        "/api/incidents",
        headers=auth_headers,
        json={"title": "API returning 500s", "description": "Spike in errors", "severity": "sev1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["severity"] == "sev1"
    assert body["status"] == "open"
    assert body["resolved_at"] is None


def test_create_incident_requires_auth(client):
    response = client.post("/api/incidents", json={"title": "No auth incident"})
    assert response.status_code == 401


def test_list_and_get_incident(client, auth_headers):
    create = client.post(
        "/api/incidents", headers=auth_headers, json={"title": "DB connection pool exhausted"}
    )
    incident_id = create.json()["id"]

    listing = client.get("/api/incidents", headers=auth_headers)
    assert listing.status_code == 200
    assert any(i["id"] == incident_id for i in listing.json())

    detail = client.get(f"/api/incidents/{incident_id}", headers=auth_headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == incident_id


def test_get_incident_not_found(client, auth_headers):
    response = client.get("/api/incidents/does-not-exist", headers=auth_headers)
    assert response.status_code == 404


def test_resolve_incident_sets_resolved_at(client, auth_headers):
    create = client.post(
        "/api/incidents", headers=auth_headers, json={"title": "Latency spike", "severity": "sev2"}
    )
    incident_id = create.json()["id"]

    update = client.patch(
        f"/api/incidents/{incident_id}", headers=auth_headers, json={"status": "resolved"}
    )
    assert update.status_code == 200
    assert update.json()["status"] == "resolved"
    assert update.json()["resolved_at"] is not None


def test_create_incident_invalid_severity(client, auth_headers):
    response = client.post(
        "/api/incidents", headers=auth_headers, json={"title": "Bad severity", "severity": "sevX"}
    )
    assert response.status_code == 422
