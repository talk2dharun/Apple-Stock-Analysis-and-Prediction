# -*- coding: utf-8 -*-
"""code.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XtX-kmToaTTuabyrxK5FX2jMmNWDuV8i
"""

from IPython import get_ipython
from IPython.display import display

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import date2num
import zipfile
import io
from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Step 1: Upload the File
uploaded = files.upload()

# Step 2: Extract and read the data
if uploaded:  # To ensure a file has been uploaded
    # To get the uploaded file name dynamically
    file_path = list(uploaded.keys())[0]

    # To check if the file is a ZIP file
    if file_path.endswith('.zip'):
        # Extract and read the CSV from the ZIP file
        with zipfile.ZipFile(io.BytesIO(uploaded[file_path]), 'r') as zip_ref:
            csv_file_name = zip_ref.namelist()[0]  # Assume the first file is the required CSV
            with zip_ref.open(csv_file_name) as csv_file:
                apple_stock_data = pd.read_csv(csv_file)
    else:
        # If it's not a ZIP file, assume it's a CSV
        apple_stock_data = pd.read_csv(io.BytesIO(uploaded[file_path]))
else:
    raise ValueError("No file uploaded. Please upload a ZIP or CSV file.")

# Step 3: Clean and Prepare the Data
apple_stock_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
apple_stock_data['Date'] = pd.to_datetime(apple_stock_data['Date'])
apple_stock_data.sort_values('Date', inplace=True)

# Convert Date to numeric format for compatibility with matplotlib
apple_stock_data['NumericDate'] = date2num(apple_stock_data['Date'])

# Rescale Volume for better visualization
apple_stock_data['Volume'] = apple_stock_data['Volume'] / 1e6  # Convert to millions

# Step 4: Visualize the Data
sns.set_theme(style="whitegrid")
plt.figure(figsize=(16, 8))

# Visualization 1: Adjusted Closing Price Over Time
plt.plot(apple_stock_data['Date'], apple_stock_data['Adj Close'], label='Adj Close', color='blue')
plt.title('Apple Stock Adjusted Closing Price Over Time', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Adjusted Close Price (USD)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

print("""The Adjusted Closing Price plot shows the trend of Apple’s adjusted stock prices over time.
This metric accounts for stock splits and dividends, providing a more accurate representation of the stock's value for comparison.
The steady upward trend indicates Apple’s strong market performance and growth over the years, punctuated by occasional market corrections.""")

# Visualization 2: Trading Volume Over Time (Adjusted Size)
plt.figure(figsize=(16, 8))
plt.fill_between(
    apple_stock_data['NumericDate'], apple_stock_data['Volume'], color='orange', alpha=0.5, label='Volume (in millions)'
)
plt.title('Apple Stock Trading Volume Over Time', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Volume (Millions of Shares)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

print("""The Trading Volume chart highlights fluctuations in the number of shares traded over time.
Peaks often coincide with significant events, such as product launches, earnings announcements, or broader market events.
Periods of higher volume indicate increased investor activity, which can signal high interest or volatility in the stock.""")

# Visualization 3: High, Low, and Close Price Comparison (Adjusted Size)
plt.figure(figsize=(16, 8))
plt.plot(apple_stock_data['Date'], apple_stock_data['High'], label='High', color='green', alpha=0.7)
plt.plot(apple_stock_data['Date'], apple_stock_data['Low'], label='Low', color='red', alpha=0.7)
plt.plot(apple_stock_data['Date'], apple_stock_data['Close'], label='Close', color='blue', alpha=0.7)
plt.title('High, Low, and Close Price Comparison', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

print("""The High, Low, and Close Price comparison provides a comprehensive view of the stock’s daily performance over time.
The High and Low values show the day’s price range, while the Close price reflects the final value at the end of trading.
This comparison is critical for understanding the stock’s volatility and daily trading behavior.\n""")  # One line gap added here

# Step 5: Predictive Modeling
# Feature Engineering
apple_stock_data['Year'] = apple_stock_data['Date'].dt.year
apple_stock_data['Month'] = apple_stock_data['Date'].dt.month
apple_stock_data['Day'] = apple_stock_data['Date'].dt.day

# Define features (X) and target (y)
X = apple_stock_data[['Year', 'Month', 'Day', 'Volume', 'High', 'Low', 'Open']]
y = apple_stock_data['Adj Close']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

# Evaluate Linear Regression Model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
print(f"Linear Regression - MSE: {mse_lr:.2f}, R²: {r2_lr:.2f}")

# Random Forest Regressor Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Evaluate Random Forest Regressor Model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"Random Forest Regressor - MSE: {mse_rf:.2f}, R²: {r2_rf:.2f}")  # No gap here

# Visualization 4: Comparison of Actual vs Predicted Prices
plt.figure(figsize=(16, 8))
plt.plot(y_test.values, label='Actual Prices', color='blue', alpha=0.7)
plt.plot(y_pred_lr, label='Predicted Prices (Linear Regression)', color='green', alpha=0.7)
plt.plot(y_pred_rf, label='Predicted Prices (Random Forest)', color='orange', alpha=0.7)
plt.title('Actual vs Predicted Adjusted Closing Prices', fontsize=14)
plt.xlabel('Test Data Index', fontsize=12)
plt.ylabel('Adjusted Close Price (USD)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

print("""The comparison of actual vs predicted prices provides a visual representation of model performance.
The Linear Regression model shows smoother predictions due to its simplicity, while the Random Forest model captures more intricate patterns,
resulting in closer alignment with actual prices in complex scenarios.""")