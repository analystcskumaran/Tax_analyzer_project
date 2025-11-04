from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Optional homepage route (for browser testing)
@app.route('/')
def home():
    return "Flask API is running. Use the /predict endpoint with a POST request."

# ✅ Main prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    income = data.get('income')
    year = data.get('year')

    # Validate inputs
    if income is None or year is None:
        return jsonify({'error': 'Missing required fields: income and year'}), 400

    try:
        income = float(income)
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Invalid input type — income must be numeric, year must be integer'}), 400

    # Simple prediction logic (replace with your ML model if needed)
    predicted_tax = round(income * 0.2, 2)

    return jsonify({'predicted_tax': predicted_tax}), 200

# ✅ Run Flask
if __name__ == "__main__":
    app.run(debug=True)
