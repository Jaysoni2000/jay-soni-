# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 22:26:21 2024

@author: BAPS
"""

import csv
import statistics
import matplotlib.pyplot as plt
from tabulate import tabulate

#This function facilitates the retrieval of demand values, offering the user the option to import data
# from a CSV file or input values manually. It prompts the user for their choice ('Y' for CSV import, 'N' for manual input),
# then proceeds accordingly. If the user opts for CSV import, they're prompted for the file path. Invalid responses prompt re-entry until
# a valid choice is made.


def get_demand_values():
    choice = input("Do you want to import demand values from a CSV file? (Y/N): ").strip().lower()
    if choice == 'y':
        file_path = input("Enter the path to the CSV file: ").strip()
        return import_demand_values_from_csv(file_path)
    elif choice == 'n':
        return input_demand_values_from_console()
    else:
        print("Invalid choice. Please enter 'Y' or 'N'.")
        return get_demand_values()

def import_demand_values_from_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            return [int(row[0]) for row in reader if row]
    except FileNotFoundError:
        print("Error: File not found.")
        return import_demand_values_from_csv()



#The input_demand_values_from_console() function collects demand values from the
# user via console input, splitting the input string by spaces to create a list of values.
# It attempts to convert each value to an integer using a list comprehension and returns 
# the resulting list of demand values. If non-numeric characters are encountered during conversion, 
# it prompts the user to re-enter numeric values.


def input_demand_values_from_console():
    values = input("Enter demand values separated by spaces: ").split()
    try:
        return [int(value) for value in values]
    except ValueError:
        print("Error: Please enter numeric values.")
        return input_demand_values_from_console()


#In the subsequent code, demand values are obtained using this function, 
#followed by the user input of the window size and alpha value via console prompts.
# Read input values



demand_values = get_demand_values()
window_size = int(input("Enter window size: "))
alpha = float(input("Enter alpha value: "))

# Check if window_size is greater than the length of demand_values
if window_size > len(demand_values):
    print("Error: Window size cannot be greater than the number of demand values.")
    exit()
# Calculate moving average
moving_averages = [round(statistics.mean(demand_values[i:i+window_size]), 2) for i in range(len(demand_values) - window_size + 1)]

# Calculate error path
error_path = [demand_values[i+window_size-1] - moving_averages[i] for i in range(len(moving_averages))]

# Calculate positive error
positive_error = [abs(error) for error in error_path]

# Calculate square error
square_error = [error ** 2 for error in positive_error]

# Calculate divide error
divide_error = [error / demand_values[i+window_size-1] for i, error in enumerate(positive_error) if i+window_size-1 < len(demand_values)]

# Prepare data for output table
output_data = list(zip(demand_values[window_size-1:], moving_averages, error_path, positive_error, square_error, divide_error))

# Display output table
output_headers = ["Demand Values", "Moving Average", "Error Path", "Positive Error", "Square Error", "Divide Error"]
print("Output Table:")
print(tabulate(output_data, headers=output_headers, tablefmt="grid"))

# Calculate mean absolute deviation (MAE)
mae = statistics.mean(positive_error)  # Exclude the first value

# Calculate mean square deviation (MSE)
mse = statistics.mean(square_error)  # Exclude the first value

# Calculate mean absolute percentage error (MAPE)
mape = statistics.mean(divide_error)  # Exclude the first value

# Prepare data for metrics table
metrics_data = [
    ["Mean Absolute Deviation (MAE)", mae],
    ["Mean Square Deviation (MSE)", mse],
    ["Mean Absolute Percentage Error (MAPE)", mape]
]

# Display metrics table
metrics_headers = ["Metrics", "Value"]
print("\nMetrics Table:")
print(tabulate(metrics_data, headers=metrics_headers, tablefmt="grid"))

# Initialize forecasted values
forecasted_values = [demand_values[0]]

# Calculate forecasted values
for i in range(1, len(demand_values)):
    forecast = alpha * demand_values[i] + (1 - alpha) * forecasted_values[-1]
    forecasted_values.append(round(forecast, 2))

# Calculate error forecasting
error_forecasting = [forecasted_values[i] - demand_values[i] for i in range(len(forecasted_values))]

# Calculate positive error forecasting
positive_error_forecasting = [abs(error) for error in error_forecasting]

# Calculate square error forecasting
square_error_forecasting = [error ** 2 for error in positive_error_forecasting]

# Calculate divide error forecasting
divide_error_forecasting = [error / demand_values[i] for i, error in enumerate(positive_error_forecasting) if i < len(demand_values)]

# Prepare data for Exponential Forecasting table with Error Forecasting, Positive Forecasting Error, Square Forecasting Error and Divide Forecasting Error
exponential_data = list(zip(demand_values, forecasted_values, error_forecasting, positive_error_forecasting, square_error_forecasting, divide_error_forecasting))

# Display Exponential Forecasting table with Error Forecasting, Positive Forecasting Error, and Divide Forecasting Error
exponential_headers = ["Demand Value", "Forecasting", "Error Forecasting", "Positive Forecasting Error", "Square Forecasting Error", "Divide Forecasting Error"]
print("\nExponential Forecasting Table:")
print(tabulate(exponential_data, headers=exponential_headers, tablefmt="grid"))

# Calculate MAE, MSE, and MAPE for Exponential Forecasting
mae_exp = statistics.mean(positive_error_forecasting[1:])  # Exclude the first value
mse_exp = statistics.mean(square_error_forecasting[1:])  # Exclude the first value
mape_exp = statistics.mean(divide_error_forecasting[1:])  # Exclude the first value

# Prepare data for Exponential Table Forecasting Error
exponential_error_data = [
    ["Mean Absolute Deviation (MAE)", mae_exp],
    ["Mean Square Deviation (MSE)", mse_exp],
    ["Mean Absolute Percentage Error (MAPE)", mape_exp]
]

# Display Exponential Table Forecasting Error
print("\nExponential Table Forecasting Error:")
print(tabulate(exponential_error_data, headers=metrics_headers, tablefmt="grid"))

# Plotting Moving Average
plt.figure(figsize=(10, 5))
plt.plot(range(window_size-1, len(demand_values)), moving_averages, label='Moving Average')
plt.xlabel('Time')
plt.ylabel('Moving Average')
plt.title('Moving Average Plot')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Forecasting Average
plt.figure(figsize=(10, 5))
plt.plot(range(len(demand_values)), forecasted_values, label='Forecasting Average')
plt.xlabel('Time')
plt.ylabel('Forecasting Average')
plt.title('Forecasting Average Plot')
plt.legend()
plt.grid(True)
plt.show()
