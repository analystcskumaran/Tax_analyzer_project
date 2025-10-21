import joblib

def test_model_load():
    model = joblib.load('models/model.pkl')
    assert model is not None