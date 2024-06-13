import csv
import sys

# Load the CSV file into a list of dictionaries
file_path = 'C:\\Users\\xae12\\Downloads\\python-portfolio-project-starter-files (1)\\python-portfolio-project-starter-files\\insurance.csv'

data = []
try:
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file path and try again.")
    sys.exit()

# Function to calculate descriptive statistics
def calculate_statistics(data, key):
    values = [float(row[key]) for row in data if row[key]]
    count = len(values)
    mean = sum(values) / count
    minimum = min(values)
    maximum = max(values)
    variance = sum((x - mean) ** 2 for x in values) / count
    std_dev = variance ** 0.5  # Square root of variance
    return count, mean, std_dev, minimum, maximum

# Function to calculate correlations
def calculate_correlation(data, key1, key2):
    values1 = [float(row[key1]) for row in data if row[key1]]
    values2 = [float(row[key2]) for row in data if row[key2]]
    mean1 = sum(values1) / len(values1)
    mean2 = sum(values2) / len(values2)
    
    covariance = sum((x - mean1) * (y - mean2) for x, y in zip(values1, values2)) / len(values1)
    std_dev1 = (sum((x - mean1) ** 2 for x in values1) / len(values1)) ** 0.5
    std_dev2 = (sum((y - mean2) ** 2 for y in values2)) ** 0.5
    
    correlation = covariance / (std_dev1 * std_dev2)
    return correlation

# Simple linear regression (one feature)
def simple_linear_regression(data, feature, target):
    X = [float(row[feature]) for row in data if row[feature]]
    y = [float(row[target]) for row in data if row[target]]
    n = len(X)
    
    mean_X = sum(X) / n
    mean_y = sum(y) / n
    
    SS_xy = sum(y_i * x_i for y_i, x_i in zip(y, X)) - n * mean_y * mean_X
    SS_xx = sum(x_i * x_i for x_i in X) - n * mean_X * mean_X
    
    slope = SS_xy / SS_xx
    intercept = mean_y - slope * mean_X
    
    return slope, intercept

# Function to predict values using linear regression
def predict(slope, intercept, X):
    return [slope * x_i + intercept for x_i in X]

# Menu options
def menu():
    print("\n\t\tMenu:")
    print("--------------------------------------------------")
    print("1. Descriptive Analysis")
    print("2. Correlation Analysis")
    print("3. Predictive Modeling (Linear Regression)")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice

# Main program loop
while True:
    choice = menu()
    
    if choice == '1':
        print("\nDescriptive Analysis")
        age_stats = calculate_statistics(data, 'age')
        bmi_stats = calculate_statistics(data, 'bmi')
        charges_stats = calculate_statistics(data, 'charges')
        
        print(f'Age statistics: {age_stats}')
        print(f'BMI statistics: {bmi_stats}')
        print(f'Charges statistics: {charges_stats}')
    
    elif choice == '2':
        print("\nCorrelation Analysis")
        age_charges_corr = calculate_correlation(data, 'age', 'charges')
        bmi_charges_corr = calculate_correlation(data, 'bmi', 'charges')
        
        print(f'Correlation between age and charges: {age_charges_corr}')
        print(f'Correlation between BMI and charges: {bmi_charges_corr}')
    
    elif choice == '3':
        print("\nPredictive Modeling (Linear Regression)")
        slope, intercept = simple_linear_regression(data, 'bmi', 'charges')
        print(f'Regression line: charges = {slope} * bmi + {intercept}')
        
        # Predict charges for test set and evaluate
        X_test = [float(row['bmi']) for row in data[:20]]  # Example test set
        y_test = [float(row['charges']) for row in data[:20]]
        y_pred = predict(slope, intercept, X_test)
        
        # Calculate Mean Squared Error (MSE)
        mse = sum((y_i - y_pred_i) ** 2 for y_i, y_pred_i in zip(y_test, y_pred)) / len(y_test)
        print(f'Mean Squared Error: {mse}')
    
    elif choice == '4':
        print("\n\nExiting the program.")
        print("your program has succefully ended")
        break
    
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
