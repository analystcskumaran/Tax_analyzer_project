import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import os

# Load data
data_path = os.path.join('..', '..', 'data', 'processed', 'cleaned_tax_data.pkl')
try:
    df = pd.read_pickle(data_path)
except FileNotFoundError:
    st.error("Data file not found.")
    st.stop()

st.title("ML Predictions")
st.write("Predict tax amounts using income and year inputs.")

income = st.slider("Income", 0, 1000000, 50000)
if 'Year' in df.columns:
    year = st.selectbox("Year", df['Year'].unique())
else:
    st.error("Column 'Year' not found.")
    st.stop()

if st.button("Predict"):
    try:
        response = requests.post('http://localhost:5000/predict', 
                                 json={'income': income, 'year': year})
        response.raise_for_status()
        pred = response.json().get('predicted_tax')
        
        if pred is not None:
            st.success(f"Predicted Tax: ${pred:.2f}")
            
            # Prediction vs. Historical Data (Scatter with available data)
            st.subheader("Prediction vs. Historical Data")
            fig = go.Figure()
            # Use available columns for plot
            if 'Bottom Bracket Taxable Income up to' in df.columns:
                fig.add_trace(go.Scatter(x=df['Bottom Bracket Taxable Income up to'], y=[pred] * len(df), 
                                         mode='markers', name='Historical Income Brackets',
                                         marker=dict(color='lightblue', size=6)))
                fig.add_trace(go.Scatter(x=[income], y=[pred], 
                                         mode='markers', name='Prediction',
                                         marker=dict(color='orange', size=12, symbol='star')))
                fig.update_layout(title="Income Bracket vs. Prediction",
                                  xaxis_title="Bottom Bracket Taxable Income up to", yaxis_title="Predicted Tax",
                                  template="plotly_white", hovermode="closest")
                st.plotly_chart(fig)
        else:
            st.warning("Prediction failed: 'predicted_tax' not in response.")
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Ensure Flask API is running on localhost:5000.")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")