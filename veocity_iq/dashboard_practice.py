# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from streamlit_echarts import st_echarts   # ECharts support
import requests   # used for news fetch in Cars Core tab

st.set_page_config(page_title="Supercar Explorer", layout="wide")

@st.cache_data
def load_default_df():
    # fallback path (the file already uploaded on server)
    try:
        return pd.read_csv('supercars_data.csv')
    except Exception:
        return pd.DataFrame()

def clean_df_basic(df):
    """
    Basic cleaning that normalizes types and strips string columns.
    """
    df = df.copy()
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
    return df

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
        st.error("No dataset found. Upload a CSV using the sidebar or place your CSV at the fallback server path ('supercars_data.csv').")
        st.stop()
    else:
        st.sidebar.info("Using provided dataset file on server")

# ------------------ FIX: strip whitespace from column names ------------------
df.columns = df.columns.str.strip()
# ----------------------------------------------------------------------------- 

# Ensure required columns exist (avoid KeyError later)
required = ['Car Name', 'Price', 'Year', 'Mileage', 'Dealer', 'Brand']
for c in required:
    if c not in df.columns:
        df[c] = pd.NA

# Basic cleaning (strip strings)
df = clean_df_basic(df)

# Robust numeric cleaning
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('[^0-9.]', '', regex=True), errors='coerce')
df['Year'] = pd.to_numeric(df['Year'].astype(str).str.extract(r'(\d{4})')[0], errors='coerce').astype('Int64')
df['Mileage'] = pd.to_numeric(df['Mileage'].astype(str).str.replace('[^0-9.]', '', regex=True), errors='coerce')

# Normalize Brand and Dealer strings
df['Brand'] = df['Brand'].astype(str).str.strip().replace({'': 'Unknown', 'nan': 'Unknown'})
df['Dealer'] = df['Dealer'].astype(str).str.strip().replace({'': 'Unknown', 'nan': 'Unknown'})

# Safe brand/dealer lists (no KeyError)
brands = sorted(df['Brand'].dropna().unique().tolist()) if df['Brand'].notna().any() else []
sel_brands = st.sidebar.multiselect("Brand", options=brands, default=brands[:8] if brands else [])

min_year = int(df['Year'].min(skipna=True)) if not df['Year'].isna().all() else 1900
max_year = int(df['Year'].max(skipna=True)) if not df['Year'].isna().all() else 2025
slider_max_year = 2025
default_upper = min(max_year, slider_max_year)
year_range = st.sidebar.slider("Year range", min_value=min_year, max_value=slider_max_year, value=(min_year, default_upper))

dealers = sorted(df['Dealer'].dropna().unique().tolist()) if df['Dealer'].notna().any() else []
sel_dealers = st.sidebar.multiselect("Dealer (optional)", options=dealers, default=[])

# Apply filters (guard against NA comparisons) — price filter removed
filtered = df.copy()
if sel_brands:
    filtered = filtered[filtered['Brand'].isin(sel_brands)]
if not filtered['Year'].isna().all():
    filtered = filtered[(filtered['Year'] >= year_range[0]) & (filtered['Year'] <= year_range[1])]
if sel_dealers:
    filtered = filtered[filtered['Dealer'].isin(sel_dealers)]

st.sidebar.markdown("---")
st.sidebar.write(f"Rows after filter: **{len(filtered):,}**")

# -----------------------------
# Top navigation: Home | Visualisation | Cars Core | Chatbot
# -----------------------------
tabs = st.tabs(["Home", "Visualisation", "Cars Core", "Chatbot"])

# -----------------------------
# HOME tab content (only this block edited as requested)
# -----------------------------
with tabs[0]:
    # Bigger "Welcome to Velocity IQ" headline (drop-in replacement)
    st.markdown(
        """
        <style>
        .vel-title {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            font-size: 80px;                /* increased size as requested */
            font-weight: 900;
            text-align: center;
            margin-bottom: 6px;
            line-height: 0.95;
            /* gradient text */
            background: linear-gradient(90deg, #9b5cff 0%, #ff5c8a 50%, #ffb86b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @media (max-width: 800px) {
            .vel-title { font-size: 40px; }
        }
        .vel-sub {
            text-align: center;
            color: #cbd5e1;
            font-size: 18px;
            margin-top: 6px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .vel-desc {
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
            color: #bfcbdc;
            text-align: center;
            font-size: 15px;
            line-height: 1.6;
            padding: 8px 18px;
            border-radius: 8px;
        }
        </style>

        <div class="vel-title">Welcome to Velocity IQ</div>
        <div class="vel-sub">Explore, compare and discover insights from a curated supercar dataset</div>
        <div class="vel-desc">
            Velocity IQ brings together car listings, pricing, dealer and brand information into one
            interactive dashboard. Filter by brand, year or dealer, hover charts for details, and
            export filtered lists. Whether you're researching market trends or building a portfolio,
            this dashboard gives you a clean, easy-to-navigate overview of the supercar market.
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# VISUALISATION tab: title + preview + charts (title and preview moved here)
# -----------------------------
with tabs[1]:
    st.title("Velocity IQ - Super Car Explorer")
    with st.expander("Preview dataset (first 10 rows)"):
        st.write("Columns:", list(df.columns))
        st.dataframe(df.head(10))

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

        # 4) Price vs Year scatter with trendline (safe hover)
        st.subheader("4. Price vs Year (scatter) with trendline")
        if filtered['Year'].notna().sum() > 0 and filtered['Price'].notna().sum() > 0:
            hover_cols = [c for c in ['Car Name', 'Dealer', 'Mileage'] if c in filtered.columns]
            try:
                fig_scatter = px.scatter(filtered, x='Year', y='Price', color='Brand', hover_data=hover_cols,
                                         title='Price vs Year', trendline='ols', labels={'Price':'Price', 'Year':'Year'})
            except Exception:
                fig_scatter = px.scatter(filtered, x='Year', y='Price', color='Brand', hover_data=hover_cols,
                                         title='Price vs Year', labels={'Price':'Price', 'Year':'Year'})
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Insufficient Year/Price data for scatter.")

        # 5) Price vs Mileage scatter coloured by Brand
        st.subheader("5. Price vs Mileage (colour = Brand)")
        if filtered['Mileage'].notna().sum() > 0 and filtered['Price'].notna().sum() > 0:
            hover_pm = [c for c in ['Car Name', 'Year', 'Dealer'] if c in filtered.columns]
            fig_pm = px.scatter(filtered, x='Mileage', y='Price', color='Brand',
                                size='Mileage', hover_data=hover_pm,
                                title='Price vs Mileage (bubble size = Mileage)')
            st.plotly_chart(fig_pm, use_container_width=True)
        else:
            st.info("Insufficient Mileage/Price data.")

        # 6) Stacked area: Price over time (binned years) — ECharts
        st.subheader("6. Stacked area: Price over time (binned years) — ECharts")
        df_year_price = filtered.dropna(subset=['Year', 'Price']).copy()
        if df_year_price.shape[0] == 0:
            st.info("Not enough Year/Price data for stacked area.")
        else:
            df_year_price['Year'] = df_year_price['Year'].astype(int)
            y_min = int(df_year_price['Year'].min())
            y_max = int(df_year_price['Year'].max())
            span = max(1, y_max - y_min)
            step = max(1, int(np.ceil(span / 10)))
            bins = list(range(y_min, y_max + step, step))
            labels = [f"{b}-{b+step-1}" for b in bins[:-1]]
            df_year_price['YearBin'] = pd.cut(df_year_price['Year'], bins=bins, labels=labels, include_lowest=True, right=False)

            top_brands = list(filtered['Brand'].value_counts().head(6).index)
            if len(top_brands) == 0:
                st.info("No brands available to plot.")
            else:
                agg = (df_year_price[df_year_price['Brand'].isin(top_brands)]
                       .groupby(['YearBin', 'Brand'], observed=True)['Price']
                       .sum()
                       .reset_index())

                pivot = agg.pivot(index='YearBin', columns='Brand', values='Price').fillna(0)
                pivot = pivot.reindex(labels, fill_value=0)

                echarts_series = []
                for brand in pivot.columns:
                    series_values = pivot[brand].astype(int).tolist()
                    echarts_series.append({
                        "name": brand,
                        "type": "line",
                        "stack": "total",
                        "areaStyle": {},
                        "emphasis": {"focus": "series"},
                        "data": series_values
                    })

                option_area = {
                    "title": {"text": "Stacked Area — Price by Brand (binned years)", "left": "center"},
                    "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
                    "legend": {"type": "scroll", "bottom": 0},
                    "toolbox": {"feature": {"saveAsImage": {}}},
                    "xAxis": {"type": "category", "boundaryGap": False, "data": labels},
                    "yAxis": {"type": "value"},
                    "series": echarts_series
                }

                st_echarts(options=option_area, height="420px")

    # RIGHT: dealer / table / quick insights + echart
    with col2:
        st.header("Dealer / Table / Quick Insights")
        st.subheader("Top Dealers by Count")
        if 'Dealer' in filtered.columns:
            dealers_count = filtered['Dealer'].value_counts().reset_index()
            dealers_count.columns = ['Dealer', 'Count']
            st.dataframe(dealers_count.head(10))
            fig_dealer = px.bar(dealers_count.head(15), x='Dealer', y='Count', title='Top Dealers by Count')
            st.plotly_chart(fig_dealer, use_container_width=True)
        else:
            st.info("No Dealer column found.")

        if 'Dealer' in filtered.columns and 'Price' in filtered.columns and filtered['Price'].notna().sum() > 0:
            dealer_price = filtered.groupby('Dealer', as_index=False)['Price'].mean().sort_values('Price', ascending=False)
            st.subheader("Average Price per Dealer (top 10)")
            st.dataframe(dealer_price.head(10))
            fig_dealer_price = px.bar(dealer_price.head(15), x='Dealer', y='Price', title='Average Price per Dealer')
            st.plotly_chart(fig_dealer_price, use_container_width=True)

        # ECharts Brand Pie (minimal & legend hidden)
        if 'Brand' in filtered.columns:
            brand_counts = filtered['Brand'].fillna("Unknown").value_counts().reset_index()
            brand_counts.columns = ['Brand', 'Count']
            echarts_data = [{"name": row["Brand"], "value": int(row["Count"])} for _, row in brand_counts.iterrows()]

            option = {
                "title": {"text": "Brand Distribution (ECharts)", "left": "center"},
                "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
                "legend": {"show": False},
                "series": [
                    {
                        "name": "Brands",
                        "type": "pie",
                        "radius": ["40%", "65%"],
                        "data": echarts_data,
                        "label": {"show": True, "position": "outside", "formatter": "{b}: {d}%", "fontSize": 12},
                        "labelLine": {"show": True},
                        "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0,0,0,0.5)"}}
                    }
                ]
            }

            st.subheader("📊 Brand Distribution (ECharts)")
            st_echarts(options=option, height="420px")

        st.markdown("---")
        st.subheader("Filtered table")
        st.dataframe(filtered.reset_index(drop=True))

        def convert_df_to_csv_bytes(df_in):
            return df_in.to_csv(index=False).encode('utf-8')

        csv_bytes = convert_df_to_csv_bytes(filtered)
        st.download_button("Download filtered data (CSV)", data=csv_bytes, file_name="supercars_filtered.csv", mime="text/csv")

        # Circular Barplot — Price by Year Bin (ECharts) (optional extra viz)
        st.subheader("Circular Barplot — Price by Year Bin (ECharts)")
        try:
            df_year_price_cb = filtered.dropna(subset=['Year', 'Price']).copy()
            if df_year_price_cb.shape[0] == 0:
                st.info("Not enough Year/Price data for circular barplot.")
            else:
                df_year_price_cb['Year'] = df_year_price_cb['Year'].astype(int)
                y_min_cb = int(df_year_price_cb['Year'].min())
                y_max_cb = int(df_year_price_cb['Year'].max())
                span_cb = max(1, y_max_cb - y_min_cb)
                step_cb = max(1, int(np.ceil(span_cb / 10)))
                bins_cb = list(range(y_min_cb, y_max_cb + step_cb, step_cb))
                labels_cb = [f"{b}-{b+step_cb-1}" for b in bins_cb[:-1]]
                df_year_price_cb['YearBin'] = pd.cut(df_year_price_cb['Year'], bins=bins_cb, labels=labels_cb, include_lowest=True, right=False)

                agg_cb = (df_year_price_cb
                          .groupby('YearBin', observed=True)['Price']
                          .sum()
                          .reindex(labels_cb, fill_value=0)
                          .astype(int)
                          .tolist())

                if sum(agg_cb) == 0:
                    st.info("Binned price sums are zero — nothing to plot.")
                else:
                    max_val = max(agg_cb)
                    scale_label = "Price"
                    display_values = agg_cb
                    if max_val >= 100000:
                        display_values = [int(v / 100000) for v in agg_cb]
                        scale_label = "Price (in 1 Lakh)"

                    option_circular = {
                        "title": {"text": "Circular Barplot — Total Price by Year Bin", "left": "center"},
                        "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
                        "angleAxis": {"type": "category", "data": labels_cb, "clockwise": False, "boundaryGap": True, "axisLabel": {"interval": 0, "rotate": 45}},
                        "radiusAxis": {"axisLabel": {"formatter": "{value}"}},
                        "polar": {},
                        "series": [
                            {
                                "type": "bar",
                                "data": display_values,
                                "coordinateSystem": "polar",
                                "name": scale_label,
                                "itemStyle": {"borderRadius": 4},
                                "label": {"show": True, "position": "inside", "formatter": "{c}"}
                            }
                        ],
                        "legend": {"show": False},
                        "toolbox": {"feature": {"saveAsImage": {}}}
                    }
                    st_echarts(options=option_circular, height="480px")
        except Exception as e_cb:
            st.info(f"Could not build circular barplot: {e_cb}")

# -----------------------------
# CARS CORE tab content (NEWS)
# -----------------------------
with tabs[2]:
    st.header("Latest Car News")

    # Put your API key in API_KEY or leave blank to skip news
    API_KEY = "f53128eb79314e71a9bd6cc98bf79276"
    news_url = f"https://newsapi.org/v2/everything?q=cars&language=en&sortBy=publishedAt&apiKey={API_KEY}"

    try:
        news_resp = requests.get(news_url, timeout=8)
        news_resp.raise_for_status()
        news_data = news_resp.json()
    except Exception:
        st.error("Failed to fetch news. Check internet/API key.")
        news_data = {"articles": []}

    articles = news_data.get("articles", [])

    if not articles:
        st.info("No news found or API limit reached.")
    else:
        for a in articles[:100]:
            title = a.get("title", "No title")
            img = a.get("urlToImage")
            desc = a.get("description", "") or ""
            link = a.get("url", "#")

            col_img, col_txt = st.columns([1, 3])
            with col_img:
                if img:
                    try:
                        st.image(img, width=300)
                    except Exception:
                        st.write("")
                else:
                    st.write("")

            with col_txt:
                st.subheader(title)
                st.write(desc)
                st.markdown(f"[Read more]({link})")

            st.markdown("---")

# -----------------------------
# CHATBOT tab content (placeholder)
# -----------------------------
with tabs[3]:
    st.header("Chatbot")
    st.write("Place your chatbot UI here. You might integrate a simple input box + responses, or link to an external chat service.")
    user_msg = st.text_input("Ask about a car (example):")
    if user_msg:
        st.write("You typed:", user_msg)
