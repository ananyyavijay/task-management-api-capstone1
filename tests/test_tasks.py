from uuid import UUID


def test_create_project(client, user_token):

    response = client.post(
        "/projects/",
        headers=user_token,
        json={
            "name": "Backend API",
            "description": "Capstone"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Backend API"


def test_get_projects(client, user_token, project):

    response = client.get(
        "/projects/",
        headers=user_token,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_task(client, user_token, project):

    response = client.post(
        "/tasks/",
        headers=user_token,
        json={
            "project_id": project["id"],
            "title": "Create Models",
            "description": "SQLAlchemy Models"
        }
    )

    assert response.status_code == 201

    data = response.json()

    UUID(data["id"])

    assert data["title"] == "Create Models"


def test_get_task(client, user_token, task):

    response = client.get(
        f"/tasks/{task['id']}",
        headers=user_token
    )

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


def test_list_tasks(client, user_token, task):

    response = client.get(
        "/tasks/",
        headers=user_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_task(client, user_token, task):

    response = client.put(
        f"/tasks/{task['id']}",
        headers=user_token,
        json={
            "title": "Updated Task",
            "status": "In Progress",
            "priority": "High"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Task"
    assert data["status"] == "In Progress"
    assert data["priority"] == "High"


def test_assign_task(client, user_token, task, second_user):

    response = client.patch(
        f"/tasks/{task['id']}/assign",
        headers=user_token,
        json={
            "assigned_to": second_user["id"]
        }
    )

    assert response.status_code == 200

    assert response.json()["assigned_to"] == second_user["id"]


def test_delete_task(client, user_token, task):

    response = client.delete(
        f"/tasks/{task['id']}",
        headers=user_token
    )

    assert response.status_code == 204


def test_deleted_task_not_found(client, user_token, task):

    client.delete(
        f"/tasks/{task['id']}",
        headers=user_token
    )

    response = client.get(
        f"/tasks/{task['id']}",
        headers=user_token
    )

    assert response.status_code == 404


def test_create_task_without_auth(client, project):

    response = client.post(
        "/tasks/",
        json={
            "project_id": project["id"],
            "title": "Unauthorized"
        }
    )

    assert response.status_code == 401


def test_assign_invalid_user(client, user_token, task):

    response = client.patch(
        f"/tasks/{task['id']}/assign",
        headers=user_token,
        json={
            "assigned_to": "11111111-1111-1111-1111-111111111111"
        }
    )

    assert response.status_code == 404


def test_update_nonexistent_task(client, user_token):

    response = client.put(
        "/tasks/11111111-1111-1111-1111-111111111111",
        headers=user_token,
        json={
            "title": "Nothing"
        }
    )

    assert response.status_code == 404