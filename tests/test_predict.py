from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_predict_requires_auth():
    payload = {
        "trip_distance": 3.0,
        "passenger_count": 1,
        "pickup_hour": 8,
        "pickup_day_of_week": 2,
        "pickup_month": 5
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 401
