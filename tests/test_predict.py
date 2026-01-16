from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_predict_with_payload():
    payload = {
        "pickuphour": 10,
        "dayof_week": 2,
        "month": 1,
        "trip_distance": 3.5,
        "PULocationID": 132,
        "DOLocationID": 45,
        "congestion_surcharge": 2.5,
        "cbd_congestion_fee": 1.0,
        "total_amount": 25.0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["estimated_duration"] > 0