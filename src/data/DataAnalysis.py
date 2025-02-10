import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Load data from a JSON file
with open("data/processed/CleanedProcessed2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert JSON data to a DataFrame
df = pd.DataFrame(data)

# Display the first few rows
print(df.head())

# Check available columns
print("Available columns:", df.columns)

# Selecting relevant variables
cols = ["price", "surface", "bedrooms", "bathrooms", "floor", "state", "municipality", "delegation", "parking", "garage", "balcony", "heating", "air_conditioning", "equipped_kitchen", "elevator"]
df = df[cols]

# Convert numeric columns
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["surface"] = pd.to_numeric(df["surface"], errors="coerce")
df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")
df["bathrooms"] = pd.to_numeric(df["bathrooms"], errors="coerce")
df["floor"] = pd.to_numeric(df["floor"], errors="coerce")

# Replace "yes"/"no" values with booleans (True/False)
boolean_cols = ["parking", "garage", "balcony", "heating", "air_conditioning", "equipped_kitchen", "elevator"]
for col in boolean_cols:
    df[col] = df[col].map({"yes": True, "no": False})

# Remove missing values
df.dropna(inplace=True)

## 3.1 Descriptive Statistics of Prices
price_mean = df["price"].mean()
price_median = df["price"].median()
price_std = df["price"].std()
price_variance = df["price"].var()
price_quartiles = df["price"].quantile([0.25, 0.5, 0.75])

print("\n📊 Apartment Price Statistics")
print(f"Mean price: {price_mean:,.2f} TND")
print(f"Median price: {price_median:,.2f} TND")
print(f"Standard deviation: {price_std:,.2f}")
print(f"Variance: {price_variance:,.2f}")
print(f"Quartiles:\n{price_quartiles}")

# Histogram of prices
plt.figure(figsize=(10,5))
sns.histplot(df["price"], bins=30, kde=True)
plt.xlabel("Price (TND)")
plt.ylabel("Frequency")
plt.title("Distribution of Apartment Prices")
plt.show()

# Boxplot of prices
plt.figure(figsize=(8,4))
sns.boxplot(x=df["price"])
plt.title("Boxplot of Apartment Prices")
plt.show()

## 3.2 Distribution Analysis of Key Variables
# Surface distribution
plt.figure(figsize=(10,5))
sns.histplot(df["surface"], bins=30, kde=True)
plt.xlabel("Surface (m²)")
plt.ylabel("Frequency")
plt.title("Distribution of Apartment Surfaces")
plt.show()

# Number of bedrooms and bathrooms
fig, axes = plt.subplots(1, 2, figsize=(12,5))
sns.countplot(x=df["bedrooms"], ax=axes[0])
axes[0].set_title("Number of Bedrooms")

sns.countplot(x=df["bathrooms"], ax=axes[1])
axes[1].set_title("Number of Bathrooms")

plt.show()

# Geographical distribution of apartments
plt.figure(figsize=(12,6))
sns.countplot(y=df["municipality"], order=df["municipality"].value_counts().index)
plt.xlabel("Number of Apartments")
plt.ylabel("Municipality")
plt.title("Geographical Distribution of Apartments")
plt.show()

## 3.3 Correlation Analysis
# Correlation matrix
plt.figure(figsize=(8,6))
corr_matrix = df[["price", "surface", "bedrooms", "bathrooms", "floor"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Matrix")
plt.show()

# Price vs. Surface
plt.figure(figsize=(10,6))
sns.scatterplot(x=df["surface"], y=df["price"])
plt.xlabel("Surface (m²)")
plt.ylabel("Price (TND)")
plt.title("Relationship between Price and Surface")
plt.show()

# Price by state
plt.figure(figsize=(12,6))
sns.boxplot(x=df["state"], y=df["price"])
plt.xlabel("State")
plt.ylabel("Price (TND)")
plt.title("Apartment Prices by State")
plt.show()
