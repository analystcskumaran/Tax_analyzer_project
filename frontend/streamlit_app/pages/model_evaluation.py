import streamlit as st
import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
import os

# Load model and data
model_path = os.path.join('..', '..', 'models', 'model.pkl')
data_path = os.path.join('..', '..', 'data', 'processed', 'cleaned_tax_data.pkl')
try:
    model = joblib.load(model_path)
    df = pd.read_pickle(data_path)
except FileNotFoundError:
    st.error("Model or data file not found.")
    st.stop()

st.title("Model Evaluation")
st.write("Evaluate the ML model's performance on test data.")

# Adjust X_test to use available columns (no 'tax_amount' for y_test, so use a placeholder or skip)
if 'Year' in df.columns and 'Bottom Bracket Taxable Income up to' in df.columns:
    X_test = df[['Year', 'Bottom Bracket Taxable Income up to']]
    # Placeholder for y_test (since 'tax_amount' isn't in dataset, use a computed or dummy value)
    y_test = df['Bottom Bracket Rate %']  # Example: predict rate instead
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    st.metric("Mean Squared Error", f"{mse:.2f}")
else:
    st.error("Required columns for evaluation not found.")

# 1. Prediction Errors (Histogram)
st.subheader("Prediction Error Distribution")
if 'y_test' in locals():
    errors = y_test - predictions
    fig = px.histogram(errors, nbins=20, 
                       title="Distribution of Prediction Errors",
                       color_discrete_sequence=px.colors.sequential.Plasma)  # Accessible
    fig.update_layout(xaxis_title="Error", yaxis_title="Frequency", template="plotly_white")
    st.plotly_chart(fig)

# 2. Feature Importance (Bar Chart)
st.subheader("Feature Importance")
if hasattr(model, 'feature_importances_') and 'X_test' in locals():
    importances = model.feature_importances_
    fig = px.bar(x=X_test.columns, y=importances, 
                 title="Feature Importances",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(xaxis_title="Feature", yaxis_title="Importance", template="plotly_white")
    st.plotly_chart(fig)
else:
    st.warning("Model does not have feature_importances_ attribute or data unavailable.")

# 3. New: Actual vs. Predicted Scatter
st.subheader("Actual vs. Predicted Values")
if 'y_test' in locals():
    fig = px.scatter(x=y_test, y=predictions, 
                     title="Actual vs. Predicted Values",
                     labels={'x': 'Actual Value', 'y': 'Predicted Value'},
                     color_discrete_sequence=px.colors.sequential.Viridis)
    fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], 
                             mode='lines', name='Perfect Fit', line=dict(color='red', dash='dash')))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig)