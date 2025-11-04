import pytest
from app import create_app, db
from app.models import Task, Comment

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# ✅ Test: Add a new task
def test_add_task(client):
    response = client.post('/tasks', json={
        "title": "Test Task",
        "description": "Testing add task"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Task"

# ✅ Test: Get all tasks
def test_get_tasks(client):
    client.post('/tasks', json={"title": "Task 1"})
    client.post('/tasks', json={"title": "Task 2"})
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

# ✅ Test: Add a comment to a task
def test_add_comment(client):
    client.post('/tasks', json={"title": "Task with comment"})
    response = client.post('/tasks/1/comments', json={"content": "Nice work"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Nice work"

# ✅ Test: Edit a task
def test_edit_task(client):
    client.post('/tasks', json={"title": "Old Task"})
    response = client.put('/tasks/1', json={"title": "Updated Task"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Task"

# ✅ Test: Delete a task
def test_delete_task(client):
    client.post('/tasks', json={"title": "Task to delete"})
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted" in data["message"].lower()
