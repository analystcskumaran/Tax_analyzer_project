import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle('../../../data/processed/cleaned_tax_data.pkl')
st.title("Tax Trends Over Time")
st.write("Visualize historical tax changes.")
st.subheader("Tax Rate Trends")
fig = px.line(df.groupby('year')['tax_rate'].mean().reset_index(), x='year', y='tax_rate', title="Average Tax Rate Over Years")
st.plotly_chart(fig)
st.subheader("Tax Rate Heatmap")
pivot = df.pivot_table(values='tax_rate', index='country', columns='year', aggfunc='mean')
fig, ax = plt.subplots()
sns.heatmap(pivot, annot=True, ax=ax)
st.pyplot(fig)