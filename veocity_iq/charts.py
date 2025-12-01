import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = pd.read_csv("all_brands_data_cleaned.csv")

# -------------------------------------------------------
# CLEAN PRICE COLUMN
# -------------------------------------------------------
# Remove commas or anything except digits
df['price_clean'] = df['Price'].astype(str).str.replace(r'[^0-9]', '', regex=True)

# Convert to integer
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

# -------------------------------------------------------
# CLEAN MILEAGE COLUMN (remove commas)
# -------------------------------------------------------
df['mileage_clean'] = df['Mileage'].astype(str).str.replace(',', '', regex=False)
df['mileage_clean'] = pd.to_numeric(df['mileage_clean'], errors='coerce')

# -------------------------------------------------------
# CLEAN BRAND COLUMN (remove extra words)
# Example: "JOE MACA FERRARI" → "FERRARI"
# -------------------------------------------------------
df['brand_clean'] = df['Brand'].astype(str).str.split().str[-1].str.upper()

# -------------------------------------------------------
# STREAMLIT APP
# -------------------------------------------------------
st.title("Supercar Analytics Dashboard")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------------------------------------
# Price Distribution Chart
# -------------------------------------------------------
clean_prices = df['price_clean'].dropna()

plt.figure(figsize=(8, 5))
plt.hist(clean_prices, bins=25)
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.title("Distribution of Car Prices")
plt.tight_layout()

st.subheader("Car Price Distribution")
st.pyplot(plt)

# -------------------------------------------------------
# Brand Frequency Chart
# -------------------------------------------------------
brand_counts = df['brand_clean'].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(brand_counts.index, brand_counts.values)
plt.xticks(rotation=45)
plt.xlabel("Brand")
plt.ylabel("Count of Cars")
plt.title("Cars Available Per Brand")
plt.tight_layout()

st.subheader("Cars Per Brand")
st.pyplot(plt)

# -------------------------------------------------------
# Mileage Distribution Chart
# -------------------------------------------------------
clean_mileage = df['mileage_clean'].dropna()

plt.figure(figsize=(8, 5))
plt.hist(clean_mileage, bins=25)
plt.xlabel("Mileage")
plt.ylabel("Frequency")
plt.title("Distribution of Car Mileage")
plt.tight_layout()

st.subheader("Mileage Distribution")
st.pyplot(plt)
