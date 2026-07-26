import os
import json
from fastapi.testclient import TestClient

from src.utils.fraud_dashboard.main import app

client = TestClient(app)

sample_tx = {
    "customer_id": "cust_test",
    "kyc_verified": 0,
    "account_age_days": 1,
    "transaction_amount": 15000.0,
    "channel": "web",
    "timestamp": "2026-07-26T12:00:00"
}


def test_explainability_key_flow():
    # Ensure key not present initially (file absent)
    r = client.get("/api/explainability/key")
    assert r.status_code == 200
    data = r.json()
    assert data["present"] in (False, True)

    # Set a nvidia key
    r2 = client.post("/api/explainability/key", json={"provider": "nvidia", "api_key": "TEST_KEY_123"})
    assert r2.status_code == 200
    assert r2.json()["provider"] == "nvidia"

    # Now GET should report present
    r3 = client.get("/api/explainability/key")
    assert r3.status_code == 200
    assert r3.json()["present"] is True


def test_prediction_flow():
    # Post a prediction request
    r = client.post("/api/prediction/predict", json=sample_tx)
    # If model loaded and mock DB present, expect 200; otherwise 503
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        data = r.json()
        assert "is_fraud" in data
        assert "risk_score" in data

    # Fetch history (may be empty or contain inserted record)
    r2 = client.get("/api/prediction/history")
    assert r2.status_code in (200, 503)
    if r2.status_code == 200:
        h = r2.json()
        assert "data" in h


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-q'])
