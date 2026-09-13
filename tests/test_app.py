import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "version" in resp.get_json()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_ready_default_true(client):
    resp = client.get("/ready")
    assert resp.status_code == 200


def test_ready_toggle(client):
    resp = client.post("/admin/ready/off")
    assert resp.status_code == 200
    resp = client.get("/ready")
    assert resp.status_code == 503

    # reset back so other tests aren't affected
    client.post("/admin/ready/on")


def test_metrics_endpoint(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"app_requests_total" in resp.data


def test_create_and_get_task(client):
    resp = client.post("/api/tasks", json={"title": "Learn Kubernetes"})
    assert resp.status_code == 201
    task = resp.get_json()
    assert task["title"] == "Learn Kubernetes"

    resp = client.get(f"/api/tasks/{task['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == task["id"]


def test_create_task_without_title(client):
    resp = client.post("/api/tasks", json={})
    assert resp.status_code == 400


def test_list_tasks(client):
    client.post("/api/tasks", json={"title": "Task A"})
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_delete_task(client):
    create_resp = client.post("/api/tasks", json={"title": "Temp task"})
    task_id = create_resp.get_json()["id"]

    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_task(client):
    resp = client.delete("/api/tasks/does-not-exist")
    assert resp.status_code == 404


def test_fail_endpoint(client):
    resp = client.get("/api/fail")
    assert resp.status_code == 500
