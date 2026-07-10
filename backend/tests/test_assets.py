"""
Test suite for the Asset API endpoints.

Covers CRUD operations, validation, error handling, and edge cases.
"""

import pytest


class TestListAssets:
    """GET /api/assets"""

    def test_returns_empty_list_initially(self, client):
        response = client.get("/api/assets")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_assets_after_creation(self, client, sample_asset):
        response = client.get("/api/assets")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["machineName"] == "Test Machine Alpha"

    def test_filter_by_status(self, client):
        client.post("/api/assets", json={"machineName": "M1", "status": "RUNNING", "uptimePercentage": 90})
        client.post("/api/assets", json={"machineName": "M2", "status": "OFFLINE", "uptimePercentage": 0})
        response = client.get("/api/assets?status=RUNNING")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "RUNNING"

    def test_search_by_name(self, client, sample_asset):
        response = client.get("/api/assets?search=Alpha")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_no_match(self, client, sample_asset):
        response = client.get("/api/assets?search=Nonexistent")
        assert response.status_code == 200
        assert len(response.json()) == 0


class TestGetAsset:
    """GET /api/assets/{id}"""

    def test_returns_existing_asset(self, client, sample_asset):
        asset_id = sample_asset["id"]
        response = client.get(f"/api/assets/{asset_id}")
        assert response.status_code == 200
        assert response.json()["machineName"] == "Test Machine Alpha"

    def test_returns_404_for_missing_asset(self, client):
        response = client.get("/api/assets/999")
        assert response.status_code == 404
        assert response.json()["error"] == "not_found"


class TestCreateAsset:
    """POST /api/assets"""

    def test_creates_asset_successfully(self, client):
        payload = {
            "machineName": "New Machine",
            "status": "RUNNING",
            "uptimePercentage": 88.5,
        }
        response = client.post("/api/assets", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["machineName"] == "New Machine"
        assert data["status"] == "RUNNING"
        assert data["uptimePercentage"] == 88.5
        assert "id" in data

    def test_defaults_status_to_running(self, client):
        response = client.post("/api/assets", json={"machineName": "Minimal"})
        assert response.status_code == 201
        assert response.json()["status"] == "RUNNING"

    def test_rejects_empty_name(self, client):
        response = client.post("/api/assets", json={"machineName": ""})
        assert response.status_code == 422

    def test_rejects_invalid_uptime(self, client):
        response = client.post(
            "/api/assets",
            json={"machineName": "Bad", "uptimePercentage": 150.0},
        )
        assert response.status_code == 422

    def test_rejects_negative_uptime(self, client):
        response = client.post(
            "/api/assets",
            json={"machineName": "Bad", "uptimePercentage": -5.0},
        )
        assert response.status_code == 422

    def test_rejects_invalid_status(self, client):
        response = client.post(
            "/api/assets",
            json={"machineName": "Bad", "status": "BROKEN"},
        )
        assert response.status_code == 422


class TestUpdateStatus:
    """PUT /api/assets/{id}/status"""

    def test_updates_status_successfully(self, client, sample_asset):
        asset_id = sample_asset["id"]
        response = client.put(
            f"/api/assets/{asset_id}/status",
            json={"status": "MAINTENANCE"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "MAINTENANCE"

    def test_returns_404_for_missing_asset(self, client):
        response = client.put(
            "/api/assets/999/status",
            json={"status": "OFFLINE"},
        )
        assert response.status_code == 404

    def test_rejects_invalid_status_value(self, client, sample_asset):
        response = client.put(
            f"/api/assets/{sample_asset['id']}/status",
            json={"status": "EXPLODED"},
        )
        assert response.status_code == 422


class TestDeleteAsset:
    """DELETE /api/assets/{id}"""

    def test_deletes_asset_successfully(self, client, sample_asset):
        asset_id = sample_asset["id"]
        response = client.delete(f"/api/assets/{asset_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/api/assets/{asset_id}")
        assert get_response.status_code == 404

    def test_returns_404_for_missing_asset(self, client):
        response = client.delete("/api/assets/999")
        assert response.status_code == 404


class TestBulkDelete:
    """POST /api/assets/bulk-delete"""

    def test_bulk_deletes_multiple_assets(self, client):
        r1 = client.post("/api/assets", json={"machineName": "A"})
        r2 = client.post("/api/assets", json={"machineName": "B"})
        r3 = client.post("/api/assets", json={"machineName": "C"})

        ids = [r1.json()["id"], r2.json()["id"]]
        response = client.post("/api/assets/bulk-delete", json={"ids": ids})
        assert response.status_code == 200
        assert response.json()["deleted"] == 2

        # C should still exist
        remaining = client.get("/api/assets")
        assert len(remaining.json()) == 1


class TestDashboardStats:
    """GET /api/assets/stats"""

    def test_returns_correct_stats(self, client):
        client.post("/api/assets", json={"machineName": "A", "status": "RUNNING", "uptimePercentage": 90})
        client.post("/api/assets", json={"machineName": "B", "status": "OFFLINE", "uptimePercentage": 0})
        client.post("/api/assets", json={"machineName": "C", "status": "MAINTENANCE", "uptimePercentage": 60})

        response = client.get("/api/assets/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_assets"] == 3
        assert data["running"] == 1
        assert data["offline"] == 1
        assert data["maintenance"] == 1
        assert data["avg_uptime"] == 50.0

    def test_returns_zero_stats_when_empty(self, client):
        response = client.get("/api/assets/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_assets"] == 0
        assert data["avg_uptime"] == 0.0


class TestHealthCheck:
    """GET /api/health"""

    def test_health_returns_healthy(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "version" in data
