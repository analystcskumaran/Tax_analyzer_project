import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ✅ Paths
raw_data_path = os.path.join("data", "raw", "tax_data.csv")
processed_dir = os.path.join("data", "processed")
model_dir = "models"
processed_path = os.path.join(processed_dir, "cleaned_tax_data.pkl")
model_path = os.path.join(model_dir, "model.pkl")

# ✅ Ensure directories exist
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)

# ✅ Load raw data
if not os.path.exists(raw_data_path):
    raise FileNotFoundError(f"❌ Data file not found at: {raw_data_path}")

print("📂 Loading data from:", raw_data_path)
df = pd.read_csv(raw_data_path, sep=';')

# ✅ Basic cleaning — drop missing values
df = df.dropna(subset=["Year", "Bottom Bracket Taxable Income up to", "Bottom Bracket Rate %"])

# ✅ Save cleaned data
df.to_pickle(processed_path)
print(f"✅ Cleaned data saved to: {processed_path}")

# ✅ Features and target
X = df[["Year", "Bottom Bracket Taxable Income up to"]]
y = df["Bottom Bracket Rate %"]

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train model
model = LinearRegression()
model.fit(X_train, y_train)

# ✅ Evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"📊 Model trained successfully | MSE = {mse:.4f}")

# ✅ Save trained model
joblib.dump(model, model_path)
print(f"✅ Model saved successfully to: {model_path}")
