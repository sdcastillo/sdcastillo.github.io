import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Better: Set path relative to script location or use current dir
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = script_dir  # or r'C:\Users\casti\OneDrive\Desktop\DataFest' if you must
os.chdir(data_dir)

# Load the data with error handling
try:
    data = pd.read_csv('Major Market Occupancy Data-revised.csv')
    leases = pd.read_csv('Leases.csv')
    price = pd.read_csv('Price and Availability Data.csv')
except FileNotFoundError as e:
    print(f"Error: {e}. Check if files exist in {data_dir}")
    exit()

# Quick inspections (keep your prints or comment out for clean run)
print(price.describe())
print("Price columns:", price.columns.tolist())
print(price['overall_rent'].describe())
print("\nFirst few rows of main data:\n", data.head())
data.info()
print("\nMarkets:", data['market'].unique())
print("\nMarket counts:\n", data['market'].value_counts())
print("\nAvg occupancy by market:\n", data.groupby('market')['avg_occupancy_proportion'].mean().sort_values(ascending=False))
print(data.describe())

# Missing values
print("\nMissing values in main data:\n", data.isnull().sum())

# Merge datasets
merged_data = data.merge(leases, on=["year", "quarter", "market"], how="left")
merged_data = merged_data.merge(price, on=["year", "quarter", "market"], how="left")
print("\nMerged columns:", merged_data.columns.tolist())

# Plotting function to avoid duplication
def plot_column(df, col):
    if col not in df.columns:
        print(f"Column '{col}' not found.")
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Histogram
    axes[0].hist(df[col].dropna(), bins=30, edgecolor='k', alpha=0.7, color='skyblue')
    axes[0].set_title(f'Histogram of {col}')
    axes[0].set_xlabel(col)
    axes[0].set_ylabel('Frequency')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Box plot
    df[[col]].boxplot(ax=axes[1])
    axes[1].set_title(f'Box Plot of {col}')
    axes[1].set_ylabel(col)
    
    # Bar plot if categorical/low unique
    if df[col].nunique() < 20:
        df[col].value_counts().plot(kind='bar', ax=axes[2], color='orange', edgecolor='black')
        axes[2].set_title(f'Bar Plot of {col}')
        axes[2].set_xlabel(col)
        axes[2].set_ylabel('Count')
    else:
        axes[2].text(0.5, 0.5, 'Too many unique values\nfor bar plot', horizontalalignment='center',
                     verticalalignment='center', transform=axes[2].transAxes, fontsize=12)
        axes[2].set_title(f'Bar Plot of {col} (Skipped)')
    
    plt.tight_layout()
    plt.show()

# Plot key columns
columns_to_plot = ['avg_occupancy_proportion', 'starting_occupancy_proportion']
for col in columns_to_plot:
    plot_column(data, col)

# Optional: Save all histograms to files instead of showing
# plt.savefig(f'histogram_{col}.png') inside loop if you want exports