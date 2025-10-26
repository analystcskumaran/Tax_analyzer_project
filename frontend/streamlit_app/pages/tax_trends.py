import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------
# Load Data
# ------------------------------
data_path = os.path.join('..', '..', 'data', 'processed', 'cleaned_tax_data.pkl')
df = pd.read_pickle(data_path)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("Tax Analyzer Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Data Exploration", "Tax Trends", "ML Predictions", "Model Evaluation"]
)

# ------------------------------
# Import page modules
# ------------------------------
from pages import data_exploration, tax_trends, ml_predictions, model_evaluation

# ------------------------------
# Home Page
# ------------------------------
if page == "Home":
    st.title("Tax Analyzer Dashboard - Home")
    st.write("Welcome! Use the sidebar to explore visualizations.")

    # Replace with your actual column names
    YEAR_COL = 'year'
    TAXRATE_COL = 'tax_rate'
    COUNTRY_COL = 'country'

    # Line chart: average tax rate by year
    if YEAR_COL in df.columns and TAXRATE_COL in df.columns:
        st.line_chart(df.groupby(YEAR_COL)[TAXRATE_COL].mean())
    else:
        st.warning(f"Columns {YEAR_COL} or {TAXRATE_COL} not found in the dataset.")

    # Bar chart: number of entries per country
    if COUNTRY_COL in df.columns:
        st.bar_chart(df[COUNTRY_COL].value_counts())
    else:
        st.warning(f"Column {COUNTRY_COL} not found in the dataset.")

# ------------------------------
# Other Pages
# ------------------------------
elif page == "Data Exploration":
    data_exploration.run(df)

elif page == "Tax Trends":
    tax_trends.run(df)

elif page == "ML Predictions":
    ml_predictions.run(df)

elif page == "Model Evaluation":
    model_evaluation.run()
