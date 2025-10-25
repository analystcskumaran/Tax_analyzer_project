from flask import Flask, request, jsonify
import joblib
import os
import traceback

app = Flask(__name__)

# ✅ Resolve model path robustly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../models/model.pkl"))

model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully from: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print(f"❌ Model file not found at: {MODEL_PATH}")

@app.route('/predict', methods=['POST'])
def predict():
    """Predict tax amount based on input JSON: {'income': ..., 'year': ...}"""
    if model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500

    try:
        data = request.get_json(force=True)

        income = data.get('income')
        year = data.get('year')

        # ✅ Input validation
        if income is None or year is None:
            return jsonify({'error': 'Missing required fields: income and year'}), 400

        # ✅ Ensure numeric values
        try:
            income = float(income)
            year = int(year)
        except ValueError:
            return jsonify({'error': 'Invalid input type — income must be numeric, year must be integer'}), 400

        # ✅ Predict safely (adjust order if your model was trained differently)
        prediction = model.predict([[income, year]])[0]

        return jsonify({'predicted_tax': float(prediction)}), 200

    except Exception as e:
        print("❌ Prediction error:\n", traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
