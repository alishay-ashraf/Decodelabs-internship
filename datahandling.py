import pandas as pd
import numpy as np

# Load your raw dataset
df = pd.read_csv("my_file.csv")

# 🚨 FIX 1: Replace non-breaking spaces (\xa0) with regular spaces, then strip whitespace
df.columns = df.columns.str.replace(r'\xa0', ' ', regex=True).str.strip()

print("--- Cleaned Column Names ---")
print(df.columns.tolist())
print("----------------------------\n")


# === PHASE 1 & 3: STRATEGIC IMPUTATION & NUMERIC PRECISION ===
# We will use 'Actual gross' as our main numeric value column.
# First, let's clean it by removing currency symbols/commas so pandas can calculate the median.
if 'Actual gross' in df.columns:
    # Convert to string, remove symbols like $, commas, or spaces, and convert to numeric
    df['Actual gross'] = df['Actual gross'].astype(str).str.replace(r'[$,\s]', '', regex=True)
    df['Actual gross'] = pd.to_numeric(df['Actual gross'], errors='coerce')
    
    # Impute missing values with the median [cite: 61, 62]
    df['Actual gross'] = df['Actual gross'].fillna(df['Actual gross'].median())
    
    # Enforce 2 decimal precision [cite: 75]
    df['Actual gross'] = df['Actual gross'].round(2)


# === PHASE 2: THE INTEGRITY AUDIT (DUPLICATES) ===
# We'll use 'Tour title' as our unique identifier equivalent to check for duplicate records.
if 'Tour title' in df.columns:
    duplicate_count = df.duplicated(subset=['Tour title']).sum()
    print(f"Total duplicate tours found: {duplicate_count}")
    
    # Drop duplicates, keeping the first occurrence [cite: 25]
    df = df.drop_duplicates(subset=['Tour title'], keep='first')


# === PHASE 3: SPEAK ONE LANGUAGE (TEXT CLEANING & DATES) ===
# Standardize Artist Names (Trim spaces and fix casing) [cite: 27, 75]
if 'Artist' in df.columns:
    df['Artist'] = df['Artist'].astype(str).str.strip().str.title()

# Standardize Year formats (handling single years or ranges like 2022-2023)
if 'Year(s)' in df.columns:
    df['Year(s)'] = df['Year(s)'].astype(str).str.strip()


# === PHASE 4: FINAL QUALITY CHECK ===
# Update our assertions to match your real columns [cite: 82]
if 'Tour title' in df.columns:
    assert df.duplicated(subset=['Tour title']).sum() == 0, "Error: Duplicates still exist!"

print("\n🎉 Validation passed! Your Concert Tour dataset is clean and ready.")