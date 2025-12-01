import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

st.title("ECharts Pie Chart - Brand")

# Load your CSV
df = pd.read_csv("supercars_data.csv")

# Clean column names (important!)
df.columns = df.columns.str.strip()

# Check if Brand column exists
if "Brand" not in df.columns:
    st.error("Column 'Brand' not found in your CSV.")
    st.write("Columns found:", list(df.columns))
    st.stop()

# Count brands
brand_counts = df["Brand"].fillna("Unknown").value_counts().reset_index()
brand_counts.columns = ["Brand", "Count"]

# ECharts data format
data = [
    {"name": row["Brand"], "value": int(row["Count"])}
    for _, row in brand_counts.iterrows()
]

# ECharts pie chart
option = {
    "title": {"text": "Brand Distribution", "left": "center"},
    "tooltip": {"trigger": "item"},
    "legend": {"orient": "vertical", "left": "left"},
    "series": [
        {
            "type": "pie",
            "radius": "60%",
            "data": data
        }
    ]
}

st_echarts(options=option, height="500px")
