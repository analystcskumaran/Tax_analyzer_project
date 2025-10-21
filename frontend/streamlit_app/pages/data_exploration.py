import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle('../../../data/processed/cleaned_tax_data.pkl')
st.title("Data Exploration")
st.write("Explore the tax dataset with charts.")
st.subheader("Tax Rate Distribution")
fig, ax = plt.subplots()
sns.histplot(df['tax_rate'], bins=20, ax=ax)
st.pyplot(fig)
st.subheader("Income vs. Tax Amount")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='income_bracket', y='tax_amount', hue='country', ax=ax)
st.pyplot(fig)
st.subheader("Data Summary")
st.dataframe(df.describe())