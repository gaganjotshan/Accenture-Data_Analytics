import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('your_file.csv')

# Display the first few rows of the DataFrame
print(df.head())

# Get information about the DataFrame, including column names and data types
print(df.info())