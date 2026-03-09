import pandas as pd
from pathlib import Path

input_file = Path("messy_data.csv")
output_file = "cleaned_data.csv"

# Create sample data if file is missing or empty
if not input_file.exists() or input_file.stat().st_size == 0:
    sample_data = """Name, Email , Age, City
Alice, alice@example.com, 25, New York
Bob, bob@example.com, , Los Angeles
Alice, alice@example.com, 25, New York
Charlie, , 30, Chicago
David, david@example.com, 22,
Emma, emma@example.com, 28, Houston
"""
    input_file.write_text(sample_data, encoding="utf-8")
    print("Created sample messy_data.csv")

df = pd.read_csv(input_file)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicates
df = df.drop_duplicates()

# Fill missing values
if "email" in df.columns:
    df["email"] = df["email"].fillna("unknown@example.com")

if "age" in df.columns:
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age"] = df["age"].fillna(df["age"].median())

if "city" in df.columns:
    df["city"] = df["city"].fillna("Unknown")

df.to_csv(output_file, index=False)

print(f"Cleaned dataset saved to {output_file}")
print("\nPreview of cleaned data:")
print(df.head())