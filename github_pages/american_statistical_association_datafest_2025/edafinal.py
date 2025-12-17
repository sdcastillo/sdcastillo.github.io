import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: set a seaborn style for nicer plots
sns.set(style="whitegrid")  # sets a white background with grid lines

# Load datasets (modify file paths as needed)
occupancy_df = pd.read_csv("Major Market Occupancy Data-revised.csv")
lease_df = pd.read_csv("Leases.csv")
rent_df = pd.read_csv("Price and Availability Data.csv")



lease_df['quarter'].unique()  # Check unique quarters in lease data

# Map quarters to corresponding start dates
quarter_to_date = {
    "Q1": "April 1",
    "Q2": "July 1",
    "Q3": "October 1",
    "Q4": "January 1"
}

# Create a new column 'month' with mapped dates
lease_df['month'] = lease_df['quarter'].map(quarter_to_date)

lease_df.to_csv("C:/Users/casti/OneDrive/Desktop/DataFest/leases_df.csv", index=False)  # Save the modified lease data

occupancy_df['month'] = occupancy_df['quarter'].map(quarter_to_date)  # Map quarters to dates in occupancy data
occupancy_df['month'].unique()  # Check unique months in occupancy data

rent_df.describe()  # Display summary statistics of the rent data

import pandas as pd

merged_data = pd.merge(occupancy_df, lease_df, how="left", on=["year", "quarter", "market"])
merged_data = pd.merge(merged_data, rent_df, how="left", on=["year", "quarter", "market"])

data_df = merged_data.copy()

rent_df['sublet_overall_rent'].describe()  # Display summary statistics of the re


print(occupancy_df.head())   # preview first 5 rows of occupancy data
print(occupancy_df.shape)    # (rows, columns) in occupancy data

print(rent_df.head())        # preview rent/price data
print(rent_df.shape)         # (rows, columns) in rent data

data_df = pd.merge(occupancy_df, rent_df, on="property_id")  # assuming we merged data
data_df.info()

data_df.describe()  # summary statistics of the merged data

#split the data into train and test sets
from sklearn.model_selection import train_test_split

#train regression model
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error, r2_score

#fit model
from sklearn.linear_model import LinearRegression

train, test = train_test_split(rent_df, test_size=0.2, random_state=42)

x_columns = ['year', 'direct_availability_proportion_y', 'available_space_y']

x_train = train[x_columns]

#replace NA with 0
x_train = x_train.fillna(0)

# Create a histogram of one of the features in the training data
plt.figure(figsize=(8, 6))
plt.hist(x_train['direct_availability_proportion_y'], bins=30, color='blue', alpha=0.7)
plt.title('Histogram of Direct Availability Proportion')
plt.xlabel('Direct Availability Proportion')
plt.ylabel('Frequency')
plt.show()
y_train = train['overall_rent_y']
y_train = y_train.fillna(0)

#find 

model = LinearRegression()
model.fit(x_train, y_train)

#summary of the model
print("Intercept:", model.intercept_)

#r square
print("R^2:", model.score(x_train, y_train))

#predict on test set
x_test = test[x_columns]

x_test = x_test.fillna(0)
y_test = test['overall_rent_y']
y_test = y_test.fillna(0)
y_pred = model.predict(x_test)      

#what are the units of 

# Calculate RMSE and R^2
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

rmse

rsquared = r2_score(y_test, y_pred)
rsquared

#train a random forest model
from sklearn.ensemble import RandomForestRegressor


rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(x_train, y_train)
rf_model.score(x_train, y_train)  


#predict on test set
rf_y_pred = rf_model.predict(x_test)        


# Calculate RMSE and R^2 for Random Forest
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_y_pred))

rf_r2 = r2_score(y_test, rf_y_pred)

rf_rmse, rf_r2

data_df.head()


data_df.to_csv("C:/Users/casti/OneDrive/Desktop/DataFestmerged_data.csv", index=False)  # Save the merged data to a CSV file