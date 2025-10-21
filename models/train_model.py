import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Load processed data
df = pd.read_pickle('data/processed/cleaned_tax_data.pkl')

# Create a target variable 'tax_amount'
# For simplicity, let's estimate tax_amount as (top_bracket_taxable_income_over * top_bracket_rate_percent / 100)
df['tax_amount'] = df['top_bracket_taxable_income_over'] * df['top_bracket_rate_percent'] / 100

# Features: we can use Year and Bottom Bracket info
X = df[['year', 'bottom_bracket_rate_percent', 'bottom_bracket_taxable_income_up_to']]
y = df['tax_amount']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Ensure model folder exists
os.makedirs('models', exist_ok=True)

# Save trained model
joblib.dump(model, 'models/model.pkl')

print("Model trained and saved to models/model.pkl")
