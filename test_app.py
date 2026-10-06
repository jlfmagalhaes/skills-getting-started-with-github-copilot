from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity = "Chess Club"
    email = "new-student@mergington.edu"

    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Missing%20Activity/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_returns_400_for_missing_registration():
    response = client.delete("/activities/Chess%20Club/unregister?email=not-registered@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
