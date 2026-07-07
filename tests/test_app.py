from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_400_when_email_not_registered():
    response = client.delete("/activities/Chess Club/signup", params={"email": "not-registered@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_get_activities_returns_no_store_cache_header():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
