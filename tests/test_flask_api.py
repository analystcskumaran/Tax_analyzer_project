from backend.flask_api import app

def test_predict():
    """Test valid prediction request"""
    client = app.test_client()
    response = client.post('/predict', json={'income': 50000, 'year': 2020})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'predicted_tax' in json_data
    assert isinstance(json_data['predicted_tax'], (float, int))

def test_predict_missing_fields():
    """Test request missing required fields"""
    client = app.test_client()
    response = client.post('/predict', json={'income': 50000})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Missing required fields: income and year'

def test_predict_invalid_types():
    """Test request with invalid types"""
    client = app.test_client()
    response = client.post('/predict', json={'income': 'abc', 'year': 'xyz'})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Invalid input type — income must be numeric, year must be integer'
