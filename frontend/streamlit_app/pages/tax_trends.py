import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =========================
# Load Data
# =========================
st.set_page_config(page_title="📉 Tax Trends", layout="wide")

data_path = os.path.join('..', '..', 'data', 'processed', 'cleaned_tax_data.pkl')
try:
    df = pd.read_pickle(data_path)
    st.sidebar.success("✅ Data loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ Data file not found at: {data_path}")
    st.stop()

st.title("📉 Tax Trends Dashboard")
st.write("Analyze trends in U.S. federal tax rates and income brackets over the years.")

# =========================
# Section 1: Bottom Bracket Rate Over Years
# =========================
st.subheader("💰 Average Bottom Bracket Rate Over the Years")
if {'Year', 'Bottom Bracket Rate %'}.issubset(df.columns):
    rate_trend = df.groupby('Year')['Bottom Bracket Rate %'].mean().reset_index()
    fig = px.line(
        rate_trend,
        x='Year', y='Bottom Bracket Rate %',
        title="Average Bottom Bracket Rate Trends",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Bottom Bracket Rate (%)",
        hovermode="x unified",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Required columns missing for rate trend plot.")

# =========================
# Section 2: Bottom Bracket Income Over Years
# =========================
st.subheader("🏦 Average Bottom Bracket Income Over the Years")
if {'Year', 'Bottom Bracket Taxable Income up to'}.issubset(df.columns):
    income_trend = df.groupby('Year')['Bottom Bracket Taxable Income up to'].mean().reset_index()
    fig = px.line(
        income_trend,
        x='Year', y='Bottom Bracket Taxable Income up to',
        title="Bottom Bracket Income Growth Over Time",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Bottom Bracket Income",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Required columns missing for income trend plot.")

# =========================
# Section 3: Correlation Heatmap
# =========================
st.subheader("📊 Correlation Heatmap of Numeric Features")
numeric_df = df.select_dtypes(include=['float64', 'int64'])

if not numeric_df.empty:
    corr = numeric_df.corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        title="Feature Correlation Matrix",
        color_continuous_scale="RdBu_r"  # ✅ Fixed color scale
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No numeric columns available for correlation analysis.")

# =========================
# Section 4: Year-over-Year Change
# =========================
st.subheader("📆 Year-over-Year Change in Bottom Bracket Rate")
if {'Year', 'Bottom Bracket Rate %'}.issubset(df.columns):
    yoy = df.groupby('Year')['Bottom Bracket Rate %'].mean().pct_change().reset_index()
    yoy.columns = ['Year', 'YoY Change']
    fig = px.bar(
        yoy,
        x='Year', y='YoY Change',
        title="Year-over-Year Change in Bottom Bracket Rate (%)",
        color='YoY Change',
        color_continuous_scale="Bluered_r"
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="YoY Change (%)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Required columns missing for YoY change plot.")

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("🧠 Developed as part of the Tax Analyzer Project – Data visualization powered by Streamlit & Plotly.")
