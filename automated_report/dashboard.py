import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Data Dashboard", layout="wide")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "data", "sample_data.csv")

@st.cache_data
def load_data():
    return pd.read_csv(data_path)

df = load_data()

st.title("📊 Automated Data Dashboard")

st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

st.header("Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", df.shape[0])
col2.metric("Total Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Rows", df.duplicated().sum())

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

if numeric_cols:
    st.header("📈 Numerical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_num = st.selectbox("Select Column", numeric_cols)
        st.write(f"Statistics for {selected_num}")
        st.dataframe(df[selected_num].describe(), use_container_width=True)
    
    with col2:
        st.write(f"Distribution: {selected_num}")
        st.bar_chart(df[selected_num].value_counts().head(20))

if len(numeric_cols) >= 2:
    st.header("🔗 Correlations")
    st.dataframe(df[numeric_cols].corr().style.background_gradient(cmap="coolwarm"), use_container_width=True)

if cat_cols:
    st.header("📁 Categorical Analysis")
    
    selected_cat = st.selectbox("Select Category Column", cat_cols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Value Counts: {selected_cat}")
        st.dataframe(df[selected_cat].value_counts(), use_container_width=True)
    
    with col2:
        st.write(f"Top 10: {selected_cat}")
        st.bar_chart(df[selected_cat].value_counts().head(10))

st.header("✅ Data Quality")
quality_df = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing": df.isnull().sum().values,
    "Missing %": (df.isnull().sum() / len(df) * 100).round(2).values,
    "Unique": df.nunique().values
})
st.dataframe(quality_df, use_container_width=True)

if numeric_cols:
    st.header("📊 Charts")
    
    chart_type = st.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Area Chart", "Scatter"])
    
    cols_to_plot = st.multiselect("Select Columns", numeric_cols, default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols)
    
    if chart_type == "Line Chart":
        st.line_chart(df[cols_to_plot])
    elif chart_type == "Bar Chart":
        st.bar_chart(df[cols_to_plot])
    elif chart_type == "Area Chart":
        st.area_chart(df[cols_to_plot])
    elif chart_type == "Scatter":
        if len(cols_to_plot) >= 2:
            st.scatter_chart(df[[cols_to_plot[0], cols_to_plot[1]]])
