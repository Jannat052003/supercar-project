import pandas as pd
import re

# Load CSV
df = pd.read_csv("all_brands_data.csv")

# cleaning the price column 
def clean_price(value):
    if pd.isna(value):
        return None

    value = str(value)

    # Remove all characters except digits
    number = re.sub(r"[^0-9]", "", value)

    return int(number) if number else None


df["Price"] = df["Price"].apply(clean_price)


# cleaning mileage
def clean_mileage(value):
    if pd.isna(value):
        return None

    value = str(value)

    # Remove commas and symbols
    number = re.sub(r"[^0-9]", "", value)

    return int(number) if number else None


df["Mileage"] = df["Mileage"].apply(clean_mileage)


# cleaning year column 
def clean_year(value):
    try:
        year = int(str(value)[:4])
        return year
    except:
        return None

df["Year"] = df["Year"].apply(clean_year)


# handling missing values
numeric_columns = ["Price", "Mileage", "Year"]

for col in numeric_columns:
    if col in df.columns:
        mean_value = df[col].dropna().mean()

        # Convert mean to integer to avoid decimals
        mean_value = int(mean_value)

        df[col] = df[col].fillna(mean_value).astype(int)

# cleaning name column 
def clean_car_name(name):
    if pd.isna(name):
        return ""

    name = str(name)

    # Remove all digits and symbols except spaces and alphabets
    # Keep only A–Z and spaces
    cleaned = re.sub(r"[^A-Za-z ]+", " ", name)

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned.upper()  # optional: convert to uppercase


df["Car Name"] = df["Car Name"].apply(clean_car_name)


# ---------- STEP: EXTRACT BRAND FROM CAR NAME ----------

brands_list = [
    "Ferrari", "Lamborghini", "Aston Martin", "Bentley", "Rolls Royce",
    "Porsche", "Mercedes", "Mercedes Benz", "BMW", "Audi", "McLaren",
    "Jaguar", "Bugatti", "Maserati", "Pagani"
]

# Sort: longest brand names first to avoid partial conflicts
brands_list = sorted(brands_list, key=len, reverse=True)

def extract_brand(name):
    name_lower = name.lower()
    for brand in brands_list:
        if brand.lower() in name_lower:
            return brand
    return "Unknown"

df["Brand"] = df["Car Name"].apply(extract_brand)

# saving the preprocessed file
df.to_csv("preprocessed_data.csv", index=False)

print("Preprocessing complete. Saved as preprocessed_data.csv")
