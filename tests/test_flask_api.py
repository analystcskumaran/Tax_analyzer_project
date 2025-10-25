import pytest
from app import app  # Import your Flask app directly

def test_predict():
    client = app.test_client()  # Use Flask test client

    # Make POST request to /predict endpoint
    response = client.post('/predict', json={'income': 50000, 'year': 2020})

    # Assert status code
    assert response.status_code == 200, f"Response error: {response.json}"

    # Assert predicted_tax is in the response
    json_data = response.get_json()
    assert 'predicted_tax' in json_data
    assert isinstance(json_data['predicted_tax'], (float, int))
