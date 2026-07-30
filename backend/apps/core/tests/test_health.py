from django.test import Client


def test_health_check_endpoint_get():
    client = Client()
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "pawmatch-backend"
    assert "environment" in data
    assert "timestamp" in data


def test_health_check_endpoint_head():
    client = Client()
    response = client.head("/health/")
    assert response.status_code == 200
    assert response.content == b""
