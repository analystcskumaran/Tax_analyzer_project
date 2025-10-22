from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# ✅ Load model safely using absolute path
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../models/model.pkl')
MODEL_PATH = os.path.abspath(MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded successfully from: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500

    try:
        data = request.get_json()
        year = data.get('year')
        income = data.get('income')

        if year is None or income is None:
            return jsonify({'error': 'Missing required fields: year and income'}), 400

        prediction = model.predict([[year, income]])[0]
        return jsonify({'predicted_tax': float(prediction)})

    except Exception as e:
        print(f"❌ Prediction error: {e}")  # Added for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)