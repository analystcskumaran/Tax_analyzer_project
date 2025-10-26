import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data
data_path = os.path.join('..', '..', 'data', 'processed', 'cleaned_tax_data.pkl')
try:
    df = pd.read_pickle(data_path)
except FileNotFoundError:
    st.error("Data file not found.")
    st.stop()

st.title("Tax Trends")
st.write("Analyze trends in tax rates and brackets over time.")

# 1. Bottom Bracket Rate Trends by Year
st.subheader("Bottom Bracket Rate Trends Over Years")
if 'Year' in df.columns and 'Bottom Bracket Rate %' in df.columns:
    fig = px.line(df.groupby('Year')['Bottom Bracket Rate %'].mean().reset_index(), 
                  x='Year', y='Bottom Bracket Rate %', 
                  title="Average Bottom Bracket Rate Trends",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(xaxis_title="Year", yaxis_title="Average Bottom Bracket Rate (%)", 
                      template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig)

# 2. Bottom Bracket Income Trends
st.subheader("Bottom Bracket Income Trends")
if 'Year' in df.columns and 'Bottom Bracket Taxable Income up to' in df.columns:
    fig = px.line(df.groupby('Year')['Bottom Bracket Taxable Income up to'].mean().reset_index(), 
                  x='Year', y='Bottom Bracket Taxable Income up to', 
                  title="Average Bottom Bracket Income Over Years",
                  color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_layout(xaxis_title="Year", yaxis_title="Average Bottom Bracket Income", 
                      template="plotly_white")
    st.plotly_chart(fig)

# 3. New: Correlation Heatmap
st.subheader("Correlation Heatmap")
numeric_df = df.select_dtypes(include=['number'])
if not numeric_df.empty:
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, 
                    title="Feature Correlations",
                    color_continuous_scale=px.colors.sequential.RdYlBu)  # Accessible scale
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig)
else:
    st.warning("No numeric columns for correlation.")

# 4. New: Year-over-Year Change in Bottom Bracket Rates
st.subheader("Year-over-Year Bottom Bracket Rate Changes")
if 'Year' in df.columns and 'Bottom Bracket Rate %' in df.columns:
    trend_df = df.groupby('Year')['Bottom Bracket Rate %'].mean().pct_change().reset_index()
    trend_df.columns = ['Year', 'YoY Change']
    fig = px.bar(trend_df, x='Year', y='YoY Change', 
                 title="Year-over-Year Percentage Change in Bottom Bracket Rates",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(xaxis_title="Year", yaxis_title="YoY Change (%)", template="plotly_white")
    st.plotly_chart(fig)