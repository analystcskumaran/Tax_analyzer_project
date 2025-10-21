import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

df = pd.read_pickle('../../../data/processed/cleaned_tax_data.pkl')
st.title("ML Predictions")
st.write("Predict tax with sliders and visualize results.")
income = st.slider("Income", 0, 1000000, 50000)
year = st.selectbox("Year", df['year'].unique())
if st.button("Predict"):
    response = requests.post('http://localhost:5000/predict', json={'income': income, 'year': year})
    pred = response.json()['predicted_tax']
    st.success(f"Predicted Tax: ${pred:.2f}")
    st.subheader("Prediction vs. Historical Data")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['income_bracket'], y=df['tax_amount'], mode='markers', name='Historical'))
    fig.add_trace(go.Scatter(x=[income], y=[pred], mode='markers', marker=dict(size=10, color='red'), name='Prediction'))
    st.plotly_chart(fig)

