import streamlit as st
import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

model = joblib.load('../../../models/model.pkl')
df = pd.read_pickle('../../../data/processed/cleaned_tax_data.pkl')
st.title("Model Evaluation")
st.write("Check ML model performance.")
X_test = df[['year', 'income_bracket']]
y_test = df['tax_amount']
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
st.metric("Mean Squared Error", f"{mse:.2f}")
st.subheader("Prediction Errors")
errors = y_test - predictions
fig, ax = plt.subplots()
ax.hist(errors, bins=20)
ax.set_title("Error Distribution")
st.pyplot(fig)
st.subheader("Feature Importance")
importances = model.feature_importances_
st.bar_chart(pd.Series(importances, index=X_test.columns))