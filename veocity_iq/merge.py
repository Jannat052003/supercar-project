import pandas as pd

# Load both cleaned datasets
df1 = pd.read_csv("preprocessed_data.csv")
df2 = pd.read_csv("preprocessed_data1.csv")

# Merge (append) them
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save final merged file
merged_df.to_csv("supercars_data.csv", index=False)

print("Merged successfully into merged_supercars_data.csv")
