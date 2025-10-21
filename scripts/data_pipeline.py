import pandas as pd

df = pd.read_csv('../data/raw/tax_data.csv')
df.dropna(inplace=True)
df['income_bracket'] = df['income_bracket'].astype(float)
df.to_pickle('../data/processed/cleaned_tax_data.pkl')
print("Data processed.")