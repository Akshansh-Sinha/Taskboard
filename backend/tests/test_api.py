from fastapi.testclient import TestClient

def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "TaskBoard API"

def test_ready(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}

def test_create_and_get_task(client: TestClient):
    create_payload = {
        "title": "Configure Prometheus",
        "description": "Set up Prometheus scraping for TaskBoard",
        "priority": "HIGH",
        "status": "TODO",
        "assignee": "DevOps Engineer"
    }
    create_resp = client.post("/api/tasks", json=create_payload)
    assert create_resp.status_code == 201
    created_task = create_resp.json()
    assert created_task["title"] == "Configure Prometheus"
    assert created_task["priority"] == "HIGH"
    task_id = created_task["id"]

    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == task_id
    assert get_resp.json()["assignee"] == "DevOps Engineer"

def test_list_tasks(client: TestClient):
    client.post("/api/tasks", json={"title": "Task 1", "priority": "LOW", "assignee": "Dev 1"})
    client.post("/api/tasks", json={"title": "Task 2", "priority": "HIGH", "assignee": "Dev 2"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

def test_update_task(client: TestClient):
    create_resp = client.post("/api/tasks", json={"title": "Original Title", "priority": "MEDIUM", "assignee": "Dev"})
    task_id = create_resp.json()["id"]

    update_payload = {"status": "IN_PROGRESS", "priority": "HIGH"}
    put_resp = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert put_resp.status_code == 200
    updated = put_resp.json()
    assert updated["status"] == "IN_PROGRESS"
    assert updated["priority"] == "HIGH"
    assert updated["title"] == "Original Title"

def test_delete_task(client: TestClient):
    create_resp = client.post("/api/tasks", json={"title": "To be deleted", "priority": "LOW", "assignee": "Dev"})
    task_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404

def test_stats_endpoint(client: TestClient):
    client.post("/api/tasks", json={"title": "T1", "status": "TODO", "priority": "LOW", "assignee": "A"})
    client.post("/api/tasks", json={"title": "T2", "status": "IN_PROGRESS", "priority": "MEDIUM", "assignee": "B"})
    client.post("/api/tasks", json={"title": "T3", "status": "DONE", "priority": "HIGH", "assignee": "C"})

    stats_resp = client.get("/api/tasks/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total"] == 3
    assert stats["todo"] == 1
    assert stats["inProgress"] == 1
    assert stats["done"] == 1

def test_task_not_found(client: TestClient):
    assert client.get("/api/tasks/99999").status_code == 404
    assert client.put("/api/tasks/99999", json={"title": "New"}).status_code == 404
    assert client.delete("/api/tasks/99999").status_code == 404
