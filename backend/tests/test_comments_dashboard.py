def test_add_comment_to_task(client, auth_headers):
    task = client.post("/api/tasks", headers=auth_headers, json={"title": "Investigate slow query"})
    task_id = task.json()["id"]

    comment = client.post(
        "/api/comments",
        headers=auth_headers,
        json={"entity_type": "task", "entity_id": task_id, "body": "Added an index, retesting."},
    )
    assert comment.status_code == 201
    assert comment.json()["entity_id"] == task_id

    listing = client.get(
        "/api/comments", headers=auth_headers, params={"entity_type": "task", "entity_id": task_id}
    )
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_comment_on_missing_entity(client, auth_headers):
    response = client.post(
        "/api/comments",
        headers=auth_headers,
        json={"entity_type": "task", "entity_id": "does-not-exist", "body": "Hello"},
    )
    assert response.status_code == 404


def test_dashboard_stats(client, auth_headers):
    client.post("/api/tasks", headers=auth_headers, json={"title": "Task A", "priority": "high"})
    client.post("/api/tasks", headers=auth_headers, json={"title": "Task B", "priority": "low"})
    client.post(
        "/api/incidents", headers=auth_headers, json={"title": "Incident A", "severity": "sev1"}
    )

    response = client.get("/api/dashboard/stats", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total_tasks"] == 2
    assert body["total_incidents"] == 1
    assert body["open_incidents"] == 1


def test_dashboard_requires_auth(client):
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 401
