# Project 02 - Cleaning messy data with pandas
# Real factory exports are never clean. This script first CREATES a messy
# file on purpose (so anyone can run it), then cleans it step by step.
# I print the shape and the problems before and after so I can see what changed.

import pandas as pd
import numpy as np

np.random.seed(1)

# ---------- step 1: make a messy csv on purpose ----------
n = 200
df = pd.DataFrame({
    "machine": np.random.choice(["Press A", "press a", "Press B", "Welder C", " Welder C "], n),
    "shift": np.random.choice(["Morning", "Evening", "Night", None], n),
    "units_made": np.random.randint(300, 700, n).astype(object),
    "defects": np.random.randint(0, 30, n).astype(object),
    "temperature": np.random.normal(70, 5, n).round(1),
})

# put in some typical problems I see in real exports
df.loc[5, "units_made"] = "  520 "          # number stored as text with spaces
df.loc[9, "units_made"] = "unknown"         # text that is not a number at all
df.loc[12, "defects"] = None                # missing value
df.loc[20, "temperature"] = 999.0           # sensor error (impossible temperature)
df.loc[33, "temperature"] = np.nan          # missing temperature
df = pd.concat([df, df.iloc[[3, 7, 11]]])   # duplicate rows

df.to_csv("messy_production.csv", index=False)
print("Made messy_production.csv with shape", df.shape)

# ---------- step 2: load it back, like I would with a real file ----------
df = pd.read_csv("messy_production.csv")
print("\n--- BEFORE cleaning ---")
print("shape:", df.shape)
print("missing values per column:")
print(df.isna().sum())
print("duplicate rows:", df.duplicated().sum())
print("machine names I found:", df["machine"].unique())

# ---------- step 3: clean, one problem at a time ----------

# 3a. duplicates - keep the first copy only
df = df.drop_duplicates()

# 3b. machine names - strip spaces and use the same capitalisation
df["machine"] = df["machine"].str.strip().str.title()

# 3c. units_made - force to number. Anything that is not a number becomes NaN
df["units_made"] = pd.to_numeric(df["units_made"], errors="coerce")

# 3d. defects - same idea
df["defects"] = pd.to_numeric(df["defects"], errors="coerce")

# 3e. impossible temperature - anything over 150 is a sensor error, so I blank it
df.loc[df["temperature"] > 150, "temperature"] = np.nan

# 3f. fill missing numbers with the median (median is safer than mean when there are outliers)
df["units_made"] = df["units_made"].fillna(df["units_made"].median())
df["defects"] = df["defects"].fillna(df["defects"].median())
df["temperature"] = df["temperature"].fillna(df["temperature"].median())

# 3g. missing shift - I don't want to invent a shift, so I label it "Unknown"
df["shift"] = df["shift"].fillna("Unknown")

# 3h. now that there are no NaN, I can make the counts whole numbers again
df["units_made"] = df["units_made"].astype(int)
df["defects"] = df["defects"].astype(int)

# ---------- step 4: check the result ----------
print("\n--- AFTER cleaning ---")
print("shape:", df.shape)
print("missing values per column:")
print(df.isna().sum())
print("duplicate rows:", df.duplicated().sum())
print("machine names now:", df["machine"].unique())
print("\nfirst rows:")
print(df.head())

df.to_csv("clean_production.csv", index=False)
print("\nSaved clean_production.csv")
