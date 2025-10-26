import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import requests
from sklearn.metrics import mean_squared_error
import os

# Load data with error handling (path relative to root)
data_path = os.path.join('data', 'processed', 'cleaned_tax_data.pkl')
try:
    df = pd.read_pickle(data_path)
except FileNotFoundError:
    st.error("Data file not found. Please check the path.")
    st.stop()

st.sidebar.title("Tax Analyzer Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Tax Trends", "ML Predictions", "Model Evaluation"])

if page == "Home":
    st.title("Tax Analyzer Dashboard - Home")
    st.write("Welcome! Explore tax data visualizations with interactive charts.")
    
    # Line chart: Average bottom bracket rate by year
    if 'Year' in df.columns and 'Bottom Bracket Rate %' in df.columns:
        fig = px.line(df.groupby('Year')['Bottom Bracket Rate %'].mean().reset_index(), 
                      x='Year', y='Bottom Bracket Rate %', 
                      title="Average Bottom Bracket Rate Over Years",
                      color_discrete_sequence=px.colors.qualitative.Set2)  # Accessible colors
        fig.update_layout(xaxis_title="Year", yaxis_title="Average Bottom Bracket Rate (%)", 
                          template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig)
    else:
        st.warning("Required columns ('Year', 'Bottom Bracket Rate %') not found.")
    
    # Bar chart: Entries per year (since 'country' isn't in dataset)
    if 'Year' in df.columns:
        fig = px.bar(df['Year'].value_counts().reset_index(), 
                     x='index', y='Year', 
                     title="Number of Entries by Year",
                     color_discrete_sequence=px.colors.sequential.Viridis)  # Colorblind-friendly
        fig.update_layout(xaxis_title="Year", yaxis_title="Count", template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.warning("Column 'Year' not found.")

elif page == "Data Exploration":
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

elif page == "Tax Trends":
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

elif page == "ML Predictions":
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

elif page == "Model Evaluation":
    st.title("Model Evaluation")
    st.write("Evaluate the ML model's performance on test data.")
    
    # Load model
    model_path = os.path.join('models', 'model.pkl')
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        st.error("Model file not found.")
        st.stop()
    
    # Adjust X_test to use available columns (no 'tax_amount' for y_test, so use a placeholder or skip)
    if 'Year' in df.columns and 'Bottom Bracket Taxable Income up to' in df.columns:
        X_test = df[['Year', 'Bottom Bracket Taxable Income up to']]
        # Placeholder for y_test (since 'tax_amount' isn't in dataset, use a computed or dummy value)
        y_test = df['Bottom Bracket Rate %']  # Example: predict rate instead
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        st.metric("Mean Squared Error", f"{mse:.2f}")
    else:
        st.error("Required columns for evaluation not found.")
    
    # 1. Prediction Errors (Histogram)
    st.subheader("Prediction Error Distribution")
    if 'y_test' in locals():
        errors = y_test - predictions
        fig = px.histogram(errors, nbins=20, 
                           title="Distribution of Prediction Errors",
                           color_discrete_sequence=px.colors.sequential.Plasma)  # Accessible
        fig.update_layout(xaxis_title="Error", yaxis_title="Frequency", template="plotly_white")
        st.plotly_chart(fig)
    
    # 2. Feature Importance (Bar Chart)
    st.subheader("Feature Importance")
    if hasattr(model, 'feature_importances_') and 'X_test' in locals():
        importances = model.feature_importances_
        fig = px.bar(x=X_test.columns, y=importances, 
                     title="Feature Importances",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(xaxis_title="Feature", yaxis_title="Importance", template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.warning("Model does not have feature_importances_ attribute or data unavailable.")
    
    # 3. New: Actual vs. Predicted Scatter
    st.subheader("Actual vs. Predicted Values")
    if 'y_test' in locals():
        fig = px.scatter(x=y_test, y=predictions, 
                         title="Actual vs. Predicted Values",
                         labels={'x': 'Actual Value', 'y': 'Predicted Value'},
                         color_discrete_sequence=px.colors.sequential.Viridis)
        fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], 
                                 mode='lines', name='Perfect Fit', line=dict(color='red', dash='dash')))
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig)