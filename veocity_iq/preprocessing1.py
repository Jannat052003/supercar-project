import pandas as pd
import re

df = pd.read_csv("dupont_supercars.csv")

# exracting car name
df["Year"] = df["Car Name"].str.extract(r"(\d{4})")

# Remove the year from Car Name
df["Car Name"] = df["Car Name"].str.replace(r"\d{4}", "", regex=True).str.strip()
df["Car Name"] = df["Car Name"].str.replace(r"\s+", " ", regex=True).str.strip()

# cleaning milegae column
df["Mileage"] = df["Mileage"].astype(str)
df["Mileage"] = df["Mileage"].str.replace(r"[^\d]", "", regex=True)
df["Mileage"] = pd.to_numeric(df["Mileage"], errors="coerce")

# Fill missing mileage with mean
mileage_mean = df["Mileage"].mean()
df["Mileage"] = df["Mileage"].fillna(mileage_mean).astype(int)

# clean price column
df["Price"] = df["Price"].astype(str)
df["Price"] = df["Price"].str.lower().replace("call for price", None)
df["Price"] = df["Price"].str.replace(r"[^\d]", "", regex=True)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Fill missing price with mean (as integer)
price_mean = int(df["Price"].mean())
df["Price"] = df["Price"].fillna(price_mean).astype(int)

# capitalizing brand column 
df["Brand"] = df["Brand"].astype(str).str.title()

# -------------------------------
# 👉 Reorder columns (only change you asked for)
# -------------------------------
df = df[["Car Name", "Brand", "Price", "Mileage", "Dealer", "Year"]]

# -------------------------------
# Save final cleaned file
# -------------------------------
df.to_csv("preprocessed_data1.csv", index=False)

print("Brand column fixed, price converted to int, and preprocessed_data1.csv created successfully!")
