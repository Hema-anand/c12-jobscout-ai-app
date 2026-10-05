from fastapi.testclient import TestClient

from app.main import app


def test_chat_returns_matches():
    with TestClient(app) as client:
        response = client.post(
            "/chat",
            json={"message": "Find Python backend jobs in Bangalore"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["request_id"]
    assert body["answer"]
    assert len(body["matched_jobs"]) >= 1


def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "jobscout_http_requests_total" in response.text
