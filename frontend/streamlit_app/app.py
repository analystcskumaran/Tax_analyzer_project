import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('../../data/processed/cleaned_tax_data.pkl')
st.sidebar.title("Tax Analyzer Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Tax Trends", "ML Predictions", "Model Evaluation"])

if page == "Home":
    st.title("Tax Analyzer Dashboard - Home")
    st.write("Welcome! Use the sidebar to explore visualizations.")
    st.line_chart(df.groupby('year')['tax_rate'].mean())
    st.bar_chart(df['country'].value_counts())
elif page == "Data Exploration":
    exec(open('pages/data_exploration.py').read())
elif page == "Tax Trends":
    exec(open('pages/tax_trends.py').read())
elif page == "ML Predictions":
    exec(open('pages/ml_predictions.py').read())
elif page == "Model Evaluation":
    exec(open('pages/model_evaluation.py').read())