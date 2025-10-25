from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    income = data.get('income')
    year = data.get('year')

    if income is None or year is None:
        return jsonify({'error': 'Missing required fields: income and year'}), 400

    try:
        income = float(income)
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Invalid input type — income must be numeric, year must be integer'}), 400

    predicted_tax = round(income * 0.2, 2)
    return jsonify({'predicted_tax': predicted_tax}), 200

if __name__ == "__main__":
    app.run(debug=True)
