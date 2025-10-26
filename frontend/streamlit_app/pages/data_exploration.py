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

st.title("Data Exploration")
st.write("Dive into the tax dataset with interactive visualizations.")

# Filter for interactivity
col1, col2 = st.columns(2)
with col1:
    if 'Year' in df.columns:
        selected_year = st.selectbox("Filter by Year", ["All"] + list(df['Year'].unique()))
    else:
        st.warning("Column 'Year' not found.")
        selected_year = "All"
with col2:
    # No 'country' column, so skip or add a placeholder
    st.write("No country filter available (column missing).")

filtered_df = df.copy()
if selected_year != "All" and 'Year' in df.columns:
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

# 1. Bottom Bracket Rate Distribution (Histogram)
st.subheader("Bottom Bracket Rate Distribution")
if 'Bottom Bracket Rate %' in filtered_df.columns:
    fig = px.histogram(filtered_df, x='Bottom Bracket Rate %', nbins=20, 
                       title="Distribution of Bottom Bracket Rates",
                       color_discrete_sequence=px.colors.sequential.Plasma,  # Accessible gradient
                       marginal="rug")
    fig.update_layout(xaxis_title="Bottom Bracket Rate (%)", yaxis_title="Frequency", template="plotly_white")
    st.plotly_chart(fig)

# 2. Bottom Bracket Income vs. Top Bracket Rate (Scatter Plot, since 'tax_amount' isn't available)
st.subheader("Bottom Bracket Income vs. Top Bracket Rate")
if 'Bottom Bracket Taxable Income up to' in filtered_df.columns and 'Top Bracket Rate %' in filtered_df.columns:
    fig = px.scatter(filtered_df, x='Bottom Bracket Taxable Income up to', y='Top Bracket Rate %', 
                     title="Bottom Bracket Income vs. Top Bracket Rate",
                     color_discrete_sequence=px.colors.qualitative.Set2)  # Distinct, accessible colors
    fig.update_layout(xaxis_title="Bottom Bracket Taxable Income up to", yaxis_title="Top Bracket Rate (%)", template="plotly_white")
    st.plotly_chart(fig)

# 3. New: Box Plot for Top Bracket Income by Year
st.subheader("Top Bracket Income Distribution by Year")
if 'Top Bracket Taxable Income Over' in filtered_df.columns and 'Year' in filtered_df.columns:
    fig = px.box(filtered_df, x='Year', y='Top Bracket Taxable Income Over', 
                 title="Box Plot of Top Bracket Income by Year",
                 color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_layout(xaxis_title="Year", yaxis_title="Top Bracket Taxable Income Over", template="plotly_white")
    st.plotly_chart(fig)

# 4. Data Summary
st.subheader("Data Summary")
st.dataframe(filtered_df.describe())