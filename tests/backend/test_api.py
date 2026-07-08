import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities_returns_all_activities_and_no_store_cache_header():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_signup_for_activity_adds_email_and_returns_message():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_for_activity_returns_400_for_duplicate_signup():
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_404():
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_removes_email():
    response = client.delete("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_for_missing_activity_returns_404():
    response = client.delete("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
