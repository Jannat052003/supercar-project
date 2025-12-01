# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Supercar Explorer", layout="wide")

@st.cache_data
def load_default_df():
    # fallback path (the file already uploaded on server)
    try:
        return pd.read_csv('supercars_data.csv')
    except Exception:
        return pd.DataFrame()

def clean_df(df):
    # Ensure numeric columns are correct types
    df = df.copy()
    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    if 'Year' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    if 'Mileage' in df.columns:
        df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
    # Normalize Brand and Dealer strings
    if 'Brand' in df.columns:
        df['Brand'] = df['Brand'].astype(str).str.strip().replace({'': 'Unknown'})
    if 'Dealer' in df.columns:
        df['Dealer'] = df['Dealer'].astype(str).str.strip().replace({'': 'Unknown'})
    return df

st.title("🚗 Supercar Explorer — Interactive Visualisations (Plotly + Streamlit)")

# --- Data load area ---
st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.sidebar.success("Loaded uploaded file")
    except Exception as e:
        st.sidebar.error(f"Can't read uploaded file: {e}")
        df = load_default_df()
else:
    df = load_default_df()
    if df.empty:
        st.error("No dataset found. Upload a CSV using the sidebar or place your CSV at the fallback server path.")
        st.stop()
    else:
        st.sidebar.info("Using provided dataset file on server")

df = clean_df(df)

# show sample and basic metrics
with st.expander("Preview dataset (first 10 rows)"):
    st.dataframe(df.head(10))

st.sidebar.header("Filters")
# Brand filter
brands = sorted(df['Brand'].dropna().unique().tolist())
sel_brands = st.sidebar.multiselect("Brand", options=brands, default=brands[:8] if brands else [])

# Year slider
min_year = int(df['Year'].min(skipna=True)) if not df['Year'].isna().all() else 1900
max_year = int(df['Year'].max(skipna=True)) if not df['Year'].isna().all() else 2025
year_range = st.sidebar.slider("Year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Price range
min_price = int(df['Price'].min(skipna=True)) if not df['Price'].isna().all() else 0
max_price = int(df['Price'].max(skipna=True)) if not df['Price'].isna().all() else 1
price_range = st.sidebar.slider("Price range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

# Dealer filter (optional)
dealers = sorted(df['Dealer'].dropna().unique().tolist())
sel_dealers = st.sidebar.multiselect("Dealer (optional)", options=dealers, default=[])

# Apply filters
filtered = df.copy()
if sel_brands:
    filtered = filtered[filtered['Brand'].isin(sel_brands)]
filtered = filtered[(filtered['Year'] >= year_range[0]) & (filtered['Year'] <= year_range[1])]
filtered = filtered[(filtered['Price'] >= price_range[0]) & (filtered['Price'] <= price_range[1])]
if sel_dealers:
    filtered = filtered[filtered['Dealer'].isin(sel_dealers)]

st.sidebar.markdown("---")
st.sidebar.write(f"Rows after filter: **{len(filtered):,}**")

# Layout: two columns main
col1, col2 = st.columns([2, 1])

# LEFT: main charts
with col1:
    st.header("Main Visualisations")
    # 1) Price distribution
    st.subheader("1. Price distribution")
    if filtered['Price'].notna().sum() > 0:
        fig_price_hist = px.histogram(filtered, x='Price', nbins=50, marginal='box',
                                      title="Price distribution (hover to inspect)", labels={'Price':'Price'})
        st.plotly_chart(fig_price_hist, use_container_width=True)
    else:
        st.info("No Price data available for histogram.")

    # 2) Avg price by brand (bar)
    st.subheader("2. Average price by Brand")
    if 'Brand' in filtered.columns and filtered['Price'].notna().sum() > 0:
        avg_brand = filtered.groupby('Brand', as_index=False)['Price'].mean().sort_values('Price', ascending=False)
        fig_avg_brand = px.bar(avg_brand, x='Brand', y='Price', title='Average Price by Brand',
                               labels={'Price':'Average Price'}, hover_data={'Price':':,.0f'})
        st.plotly_chart(fig_avg_brand, use_container_width=True)
    else:
        st.info("Insufficient Brand/Price data.")

    # 3) Count by Brand
    st.subheader("3. Count of cars per Brand")
    if 'Brand' in filtered.columns:
        cnt_brand = filtered['Brand'].value_counts().reset_index()
        cnt_brand.columns = ['Brand', 'Count']
        fig_cnt_brand = px.bar(cnt_brand, x='Brand', y='Count', title='Number of Cars per Brand')
        st.plotly_chart(fig_cnt_brand, use_container_width=True)
    else:
        st.info("No Brand column available.")

    # 4) Price vs Year scatter with trendline
    st.subheader("4. Price vs Year (scatter) with trendline")
    if filtered['Year'].notna().sum() > 0 and filtered['Price'].notna().sum() > 0:
        fig_scatter = px.scatter(filtered, x='Year', y='Price', color='Brand', hover_data=['Car Name','Dealer','Mileage'],
                                 title='Price vs Year', trendline='ols', labels={'Price':'Price', 'Year':'Year'})
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Insufficient Year/Price data for scatter.")

    # 5) Price vs Mileage scatter coloured by Brand
    st.subheader("5. Price vs Mileage (colour = Brand)")
    if filtered['Mileage'].notna().sum() > 0 and filtered['Price'].notna().sum() > 0:
        fig_pm = px.scatter(filtered, x='Mileage', y='Price', color='Brand',
                            size='Mileage', hover_data=['Car Name','Year','Dealer'],
                            title='Price vs Mileage (bubble size = Mileage)')
        st.plotly_chart(fig_pm, use_container_width=True)
    else:
        st.info("Insufficient Mileage/Price data.")

    # 6) Bubble chart: Price vs Year (size = Mileage)
    st.subheader("6. Bubble chart: Price vs Year (bubble = Mileage)")
    if filtered[['Year','Price','Mileage']].dropna().shape[0] > 0:
        fig_bubble = px.scatter(filtered.dropna(subset=['Year','Price','Mileage']),
                                x='Year', y='Price', size='Mileage', color='Brand',
                                hover_name='Car Name', title='Bubble: Price vs Year (size=Mileage)')
        st.plotly_chart(fig_bubble, use_container_width=True)
    else:
        st.info("Not enough complete rows for bubble chart.")

# RIGHT: dealer / table / details
with col2:
    st.header("Dealer / Table / Quick Insights")
    # Dealer counts
    st.subheader("Top Dealers by Count")
    if 'Dealer' in filtered.columns:
        dealers_count = filtered['Dealer'].value_counts().reset_index().rename(columns={'index':'Dealer','Dealer':'Count'})
        st.dataframe(dealers_count.head(10))
        fig_dealer = px.bar(dealers_count.head(15), x='Dealer', y='Count', title='Top Dealers by Count')
        st.plotly_chart(fig_dealer, use_container_width=True)
    else:
        st.info("No Dealer column found.")

    # Average price per dealer
    if 'Dealer' in filtered.columns and 'Price' in filtered.columns:
        dealer_price = filtered.groupby('Dealer', as_index=False)['Price'].mean().sort_values('Price', ascending=False)
        st.subheader("Average Price per Dealer (top 10)")
        st.dataframe(dealer_price.head(10))
        fig_dealer_price = px.bar(dealer_price.head(15), x='Dealer', y='Price', title='Average Price per Dealer')
        st.plotly_chart(fig_dealer_price, use_container_width=True)

    st.markdown("---")
    st.subheader("Filtered table")
    st.dataframe(filtered.reset_index(drop=True))

    # CSV download
    def convert_df_to_csv_bytes(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_bytes = convert_df_to_csv_bytes(filtered)
    st.download_button("Download filtered data (CSV)", data=csv_bytes, file_name="supercars_filtered.csv", mime="text/csv")

# Footer tips
st.markdown("""
---
**Tips:**  
- Use the sidebar filters to focus on specific brands, years, price ranges, or dealers.  
- Hover on points to see detailed info (Car Name, Dealer, Mileage).  
- You can export any filtered subset via the download button.
""")
