import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Set working directory (adjust path as needed)
os.chdir(r'C:\Users\casti\OneDrive\Desktop\DataFest')

# Load the data
file_path = 'Major Market Occupancy Data-revised.csv'
data = pd.read_csv(file_path)

leases = pd.read_csv('Leases.csv')
price = pd.read_csv('Price and Availability Data.csv')

# Quick inspections
print(price.describe())  # Describe statistics for price DataFrame
print(price.columns)
print(price['overall_rent'].describe())

print(data.head())
data.info()

print(data.columns)
print(data['market'].unique())
print(data['market'].value_counts())

print(data.groupby('market')['avg_occupancy_proportion'].mean().sort_values(ascending=False))
print(data.describe())

# Check for missing values
missing_values = data.isnull().sum()
print("Missing values:\n", missing_values)

print("Unique quarters:", data['quarter'].unique())
print("Mean starting occupancy proportion:", data['starting_occupancy_proportion'].mean())

# Merge datasets on shared columns
merged_data = data.merge(leases, on=["year", "quarter", "market"], how="left")
merged_data = merged_data.merge(price, on=["year", "quarter", "market"], how="left")

print("Merged DataFrame columns:\n", merged_data.columns)

# Create histograms for all numeric columns in merged_data
numeric_columns = merged_data.select_dtypes(include=[np.number]).columns
for column in numeric_columns:
    plt.figure(figsize=(8, 6))
    plt.hist(merged_data[column].dropna(), bins=30, edgecolor='k', alpha=0.7)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Box plot, Histogram, and Bar plot for selected columns in data
columns_to_plot = ['avg_occupancy_proportion', 'starting_occupancy_proportion']
for col in columns_to_plot:
    if col in data.columns:
        # Box Plot
        plt.figure(figsize=(6, 4))
        data.boxplot(column=col)
        plt.title(f'Box Plot of {col}')
        plt.ylabel(col)
        plt.tight_layout()
        plt.show()

        # Histogram
        plt.figure(figsize=(6, 4))
        plt.hist(data[col].dropna(), bins=30, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

        # Bar Plot (if the column has few unique values)
        if data[col].nunique() < 20:
            plt.figure(figsize=(8, 5))
            data[col].value_counts().plot(kind='bar', color='orange', edgecolor='black')
            plt.title(f'Bar Plot of {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.tight_layout()
            plt.show()
    else:
        print(f"Column '{col}' not found in the dataset.")
