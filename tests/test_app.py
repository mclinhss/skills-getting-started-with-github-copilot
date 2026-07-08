from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_participant_returns_400_when_email_not_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_get_activities_returns_no_store_cache_header():
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
