import joblib
from sklearn.metrics import mean_squared_error
import pandas as pd

model = joblib.load('model.pkl')
df = pd.read_pickle('../data/processed/cleaned_tax_data.pkl')
X_test = df[['year', 'income_bracket']]
y_test = df['tax_amount']
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"MSE: {mse}")