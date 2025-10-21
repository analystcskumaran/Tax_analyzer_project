import pandas as pd
import os

# Ensure processed folder exists
os.makedirs('data/processed', exist_ok=True)

# Load CSV with correct delimiter
df = pd.read_csv('data/raw/tax_data.csv', sep=';')

# Drop completely empty columns (like the extra ;; at the end)
df = df.dropna(axis=1, how='all')

# Optional: normalize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('%', 'percent')

# Example: convert numeric columns to float
numeric_cols = ['bottom_bracket_rate_percent', 
                'bottom_bracket_taxable_income_up_to', 
                'top_bracket_rate_percent', 
                'top_bracket_taxable_income_over']
for col in numeric_cols:
    df[col] = df[col].astype(float)

# Save processed data as pickle
pickle_path = 'data/processed/cleaned_tax_data.pkl'
df.to_pickle(pickle_path)

print(f"Data processed successfully. Pickle saved at: {pickle_path}")
