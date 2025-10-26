import pandas as pd
import os

# Your dataset as a string (copy-paste from your message)
data_string = """Year;Bottom Bracket Rate %;Bottom Bracket Taxable Income up to;Top Bracket Rate %;Top Bracket Taxable Income Over;;
2020;10;19400;37;622050;;
2019;10;19400;37;612350;;
2018;10;19050;37;600000;;
2017;10;18650;39.6;470700;;
2016;10;18550;39.6;466950;;
2015;10;18450;39.6;464850;;
2014;10;18150;39.6;457600;;
2013;10;17850;39.6;450000;;
2012;10;17400;35;388350;;"""

# Convert to DataFrame, selecting only the first 5 columns to avoid 'Unnamed' extras
from io import StringIO
df = pd.read_csv(StringIO(data_string), sep=';', usecols=[0, 1, 2, 3, 4])

# Clean column names (remove trailing spaces if any)
df.columns = df.columns.str.strip()

# Optional: Convert numeric columns to appropriate types
df['Year'] = df['Year'].astype(int)
df['Bottom Bracket Rate %'] = df['Bottom Bracket Rate %'].astype(float)
df['Bottom Bracket Taxable Income up to'] = df['Bottom Bracket Taxable Income up to'].astype(int)
df['Top Bracket Rate %'] = df['Top Bracket Rate %'].astype(float)
df['Top Bracket Taxable Income Over'] = df['Top Bracket Taxable Income Over'].astype(int)

# Ensure the processed folder exists
os.makedirs('data/processed', exist_ok=True)

# Save as pickle
df.to_pickle('data/processed/cleaned_tax_data.pkl')

print("Pickle file created successfully!")
print("Columns:", df.columns.tolist())
print(df.head())