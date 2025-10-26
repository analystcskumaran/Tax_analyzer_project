import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import os

# 1. FIX: Ensure data path is relative to the project root or adjust for running from 'pages'
# The triple '..' suggests going up three directories, likely to the project root.
# We keep the original path structure, assuming it leads to D:\Devops_project\data\processed\...
try:
    # NOTE: This path is highly dependent on where Streamlit is run from.
    # If run from the root D:\Devops_project, it should be './data/processed/cleaned_tax_data.pkl'
    # Since this file is in 'pages', the '...' is likely correct to reach the root.
    df = pd.read_pickle('../../../data/processed/cleaned_tax_data.pkl')
except FileNotFoundError:
    st.error("Error loading data. Check the path to 'cleaned_tax_data.pkl'.")
    st.stop()
    
st.title("ML Predictions")
st.write("Predict tax with sliders and visualize results.")

# Ensure income is correctly scaled for display/model input if necessary
income = st.slider("Income", 0, 1000000, 50000)

# 2. FIXED: Uses the corrected 'Year' column name (Capital Y)
year = st.selectbox("Year", df['Year'].unique())

if st.button("Predict"):
    # 3. CRITICAL FIX: Changed 'Year' (uppercase variable) to 'year' (lowercase variable)
    # The variable defined by st.selectbox is 'year'.
    try:
        response = requests.post('http://localhost:5000/predict', 
                                 json={'income': income, 'year': year}) 
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        pred = response.json().get('predicted_tax')

        if pred is not None:
            st.success(f"Predicted Tax: ${pred:.2f}")
            st.subheader("Prediction vs. Historical Data")
            
            # --- Plotting ---
            fig = go.Figure()
            # ASSUMPTION: df contains 'income_bracket' and 'tax_amount' columns for the plot
            fig.add_trace(go.Scatter(x=df['income_bracket'], y=df['tax_amount'], 
                                    mode='markers', name='Historical'))
            fig.add_trace(go.Scatter(x=[income], y=[pred], 
                                    mode='markers', marker=dict(size=10, color='red'), 
                                    name='Prediction'))
            fig.update_layout(xaxis_title="Income Bracket", yaxis_title="Tax Amount")
            st.plotly_chart(fig)
        else:
             st.warning("Prediction received but 'predicted_tax' key was missing in API response.")

    except requests.exceptions.ConnectionError:
        st.error("🔴 Connection Error: Could not connect to the Flask API. Please ensure your Flask application is running on http://localhost:5000.")
    except requests.exceptions.RequestException as e:
        st.error(f"🔴 API Request Error: {e}. Check the Flask API logs.")
