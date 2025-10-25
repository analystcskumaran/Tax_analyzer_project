import requests
import time

def test_predict():
    # Wait for Flask to start
    time.sleep(5)
    response = requests.post('http://localhost:5000/predict', json={'income': 50000, 'year': 2020})
    assert response.status_code == 200
    assert 'predicted_tax' in response.json()