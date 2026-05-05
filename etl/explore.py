import pandas as pd

df = pd.read_csv(r"C:\Users\User\Documents\REPOSITORY\superstore-etl\data\train.csv")

print("=== ROWS WITH NULL POSTAL CODE ===")
print(df[df["Postal Code"].isnull()][["Order ID", "City", "State", "Postal Code"]].to_string())

print("\n=== UNIQUE VALUES ===")
print(f"Ship Modes: {df['Ship Mode'].unique().tolist()}")
print(f"Segments: {df['Segment'].unique().tolist()}")
print(f"Categories: {df['Category'].unique().tolist()}")
print(f"Sub-Categories: {df['Sub-Category'].unique().tolist()}")
print(f"Regions: {df['Region'].unique().tolist()}")
print(f"Countries: {df['Country'].nunique()}")
print(f"Date format sample: {df['Order Date'].head(5).tolist()}")
print(f"Order Date Format: {df['Order Date'].dtype}")
print(f"Ship Date Format: {df['Ship Date'].dtype}")
print(f"\n=== POSTAL CODE dtype check ===")
print(f"Postal Code dtype: {df['Postal Code'].dtype}")
