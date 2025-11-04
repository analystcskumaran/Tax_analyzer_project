import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import requests
from sklearn.metrics import mean_squared_error
import os

# =========================
# Streamlit Setup
# =========================
st.set_page_config(page_title="Tax Analyzer Dashboard", layout="wide")
st.title("💼 Tax Analyzer Dashboard")

# =========================
# Load Dataset (Auto-Detect)
# =========================
# Tries multiple possible paths for flexibility
possible_paths = [
    os.path.join('data', 'raw', 'tax_data.csv'),
    os.path.join('..', 'data', 'raw', 'tax_data.csv'),
    os.path.join('..', '..', 'data', 'raw', 'tax_data.csv'),
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        break

if not data_path:
    st.error("❌ Could not find 'tax_data.csv'. Please ensure it's placed in one of these locations:\n\n"
             "• ./data/raw/tax_data.csv\n• ../data/raw/tax_data.csv\n• ../../data/raw/tax_data.csv")
    st.stop()

try:
    df = pd.read_csv(data_path, delimiter=';')
    st.sidebar.success(f"✅ Data loaded successfully from: {data_path}")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# =========================
# Clean & Convert Data
# =========================
df.columns = df.columns.str.strip()

numeric_cols = [
    "Bottom Bracket Rate %",
    "Bottom Bracket Taxable Income up to",
    "Top Bracket Rate %",
    "Top Bracket Taxable Income Over"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[^\d.\-]", "", regex=True)
            .replace("", pd.NA)
            .astype(float)
        )

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Tax Trends", "ML Predictions", "Model Evaluation"])

# =========================
# HOME PAGE
# =========================
if page == "Home":
    st.header("🏠 Welcome to the Tax Analyzer Dashboard")
    st.write("Explore U.S. federal tax rate trends interactively over the years!")

    col1, col2, col3 = st.columns(3)
    if 'Year' in df.columns and 'Bottom Bracket Rate %' in df.columns:
        col1.metric("📅 Total Years", df["Year"].nunique())
        col2.metric("💰 Avg Bottom Rate (%)", round(df["Bottom Bracket Rate %"].mean(), 2))
        col3.metric("📈 Max Top Rate (%)", df["Top Bracket Rate %"].max())

    # Chart 1
    if 'Year' in df.columns and 'Bottom Bracket Rate %' in df.columns:
        fig = px.line(df.groupby('Year')['Bottom Bracket Rate %'].mean().reset_index(),
                      x='Year', y='Bottom Bracket Rate %',
                      title="Average Bottom Bracket Rate Over Years",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    # Chart 2
    if 'Year' in df.columns:
        year_counts = df['Year'].value_counts().reset_index()
        year_counts.columns = ['Year', 'Count']
        fig = px.bar(year_counts, x='Year', y='Count',
                     title="Number of Entries by Year",
                     color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA EXPLORATION
# =========================
elif page == "Data Exploration":
    st.header("🔍 Explore the Tax Data")

    selected_year = st.selectbox("Select Year", ["All"] + sorted(df["Year"].unique().tolist()))

    filtered_df = df if selected_year == "All" else df[df["Year"] == selected_year]

    # Histogram
    if 'Bottom Bracket Rate %' in filtered_df.columns:
        fig = px.histogram(filtered_df, x='Bottom Bracket Rate %', nbins=10,
                           color_discrete_sequence=px.colors.sequential.Plasma,
                           title="Distribution of Bottom Bracket Rates")
        st.plotly_chart(fig, use_container_width=True)

    # Scatter
    if {'Bottom Bracket Taxable Income up to', 'Top Bracket Rate %'}.issubset(filtered_df.columns):
        fig = px.scatter(filtered_df, x='Bottom Bracket Taxable Income up to', y='Top Bracket Rate %',
                         color='Year', size='Bottom Bracket Rate %',
                         title="Income vs Top Bracket Rate by Year")
        st.plotly_chart(fig, use_container_width=True)

    # Box Plot
    if 'Top Bracket Taxable Income Over' in filtered_df.columns:
        fig = px.box(filtered_df, x='Year', y='Top Bracket Taxable Income Over',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     title="Top Bracket Income by Year")
        st.plotly_chart(fig, use_container_width=True)

    # Summary
    st.subheader("🧾 Summary Statistics")
    st.dataframe(filtered_df.describe())

# =========================
# TAX TRENDS
# =========================
elif page == "Tax Trends":
    st.header("📉 Tax Rate Trends")

    if 'Bottom Bracket Rate %' in df.columns:
        fig = px.line(df.groupby('Year')['Bottom Bracket Rate %'].mean().reset_index(),
                      x='Year', y='Bottom Bracket Rate %',
                      title="Average Bottom Bracket Rate Over Time")
        st.plotly_chart(fig, use_container_width=True)

    if 'Bottom Bracket Taxable Income up to' in df.columns:
        fig = px.line(df.groupby('Year')['Bottom Bracket Taxable Income up to'].mean().reset_index(),
                      x='Year', y='Bottom Bracket Taxable Income up to',
                      title="Average Bottom Bracket Income Over Time")
        st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("📊 Correlation Heatmap")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    if not numeric_df.empty:
        fig = px.imshow(
            numeric_df.corr(),
            text_auto=True,
            color_continuous_scale=px.colors.diverging.RdYlBu,  # ✅ Fixed here
            title="Feature Correlations"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric columns found for correlation analysis.")


    st.subheader("📆 YoY Change in Bottom Bracket Rate")
    trend_df = df.groupby('Year')['Bottom Bracket Rate %'].mean().pct_change().reset_index()
    trend_df.columns = ['Year', 'YoY Change']
    fig = px.bar(trend_df, x='Year', y='YoY Change',
                 title="Year-over-Year % Change in Bottom Bracket Rates",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# ML PREDICTIONS
# =========================
elif page == "ML Predictions":
    st.header("🤖 Tax Prediction Engine")

    income = st.slider("Select Income", 0, 1_000_000, 50_000)
    year = st.selectbox("Select Year", sorted(df["Year"].unique().tolist()))

    if st.button("Predict"):
        try:
            response = requests.post("http://localhost:5000/predict",
                                     json={"income": income, "year": year})
            response.raise_for_status()
            pred = response.json().get("predicted_tax")

            if pred is not None:
                st.success(f"Predicted Tax: ${pred:,.2f}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Flask API not running. Please start backend server.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# =========================
# MODEL EVALUATION
# =========================
