def test_create_task(client, auth_headers):
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Fix flaky CI job", "description": "Investigate flaky test", "priority": "high"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Fix flaky CI job"
    assert body["status"] == "todo"
    assert body["priority"] == "high"


def test_create_task_requires_auth(client):
    response = client.post("/api/tasks", json={"title": "No auth task"})
    assert response.status_code == 401


def test_create_task_invalid_input(client, auth_headers):
    # title is required and must be non-empty
    response = client.post("/api/tasks", headers=auth_headers, json={"title": ""})
    assert response.status_code == 422


def test_list_and_get_task(client, auth_headers):
    create = client.post("/api/tasks", headers=auth_headers, json={"title": "Deploy service"})
    task_id = create.json()["id"]

    listing = client.get("/api/tasks", headers=auth_headers)
    assert listing.status_code == 200
    assert any(t["id"] == task_id for t in listing.json())

    detail = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == task_id


def test_get_task_not_found(client, auth_headers):
    response = client.get("/api/tasks/does-not-exist", headers=auth_headers)
    assert response.status_code == 404


def test_update_task_status(client, auth_headers):
    create = client.post("/api/tasks", headers=auth_headers, json={"title": "Patch server"})
    task_id = create.json()["id"]

    update = client.patch(
        f"/api/tasks/{task_id}", headers=auth_headers, json={"status": "in_progress"}
    )
    assert update.status_code == 200
    assert update.json()["status"] == "in_progress"


def test_update_task_invalid_status_rejected(client, auth_headers):
    create = client.post("/api/tasks", headers=auth_headers, json={"title": "Patch server"})
    task_id = create.json()["id"]

    update = client.patch(
        f"/api/tasks/{task_id}", headers=auth_headers, json={"status": "not_a_real_status"}
    )
    assert update.status_code == 422


def test_delete_task(client, auth_headers):
    create = client.post("/api/tasks", headers=auth_headers, json={"title": "Temp task"})
    task_id = create.json()["id"]

    delete = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert delete.status_code == 204

    get_after = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert get_after.status_code == 404
