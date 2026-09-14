from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_request_missing_request_id():
    response = client.post(
        "/analyze-request",
        json={
            "message": "We need 10 glass panels for our office."
        },
    )

    assert response.status_code == 422


def test_analyze_request_missing_message():
    response = client.post(
        "/analyze-request",
        json={
            "request_id": "REQ-1001"
        },
    )

    assert response.status_code == 422


def test_analyze_request_empty_message():
    response = client.post(
        "/analyze-request",
        json={
            "request_id": "REQ-1001",
            "message": "",
        },
    )

    assert response.status_code == 422