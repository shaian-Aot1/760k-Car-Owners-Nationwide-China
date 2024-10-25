!pip install pandas
!pip install googletrans==3.1.0a0

import pandas as pd
from googletrans import Translator
import math

# Initialize the translator
translator = Translator()

# Load the CSV file into a pandas DataFrame
csv_file_path = '/content/760k-Car-Owners-Nationwide-China-csv-2020.csv'
# Try different encodings or use 'latin1' as a fallback
try:
    df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python')  # First try utf-8
except UnicodeDecodeError:
    try:
        df = pd.read_csv(csv_file_path, encoding='gbk', engine='python')  # Then try gbk (common for Chinese text)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='latin1', engine='python')  # Fallback to latin1

# Function to batch translate text
def batch_translate_text(text_list):
    # Filter out any empty or None values before translation
    text_list = [text if text else '' for text in text_list]  # Replace None with empty string
    
    # Join all texts into a single string, separating each with a delimiter
    text_combined = '\n'.join(text_list)

    try:
        # Translate the combined text from Chinese to English
        translated = translator.translate(text_combined, src='zh-cn', dest='en')
        # Split the result back into individual translations
        return translated.text.split('\n')
    except Exception as e:
        print(f"Error translating batch: {e}")
        # If translation fails, return the original list
        return text_list

# Step 1: Remove empty columns from the DataFrame
df = df.dropna(axis=1, how='all')  # Drop columns where all values are NaN

# Step 2: Translate the column headers directly and replace them
translated_columns = batch_translate_text(df.columns.tolist())
df.columns = translated_columns  # Overwrite the original column names with the translated ones

# Step 3: Translate the first 5 rows of the DataFrame
df_subset = df.head(5).copy()  # Select the first 5 rows

columns_to_translate = df.columns.tolist()

for column in columns_to_translate:
    try:
        column_values = df_subset[column].fillna('').astype(str).tolist()  # Ensure no NaN values and convert to string
    except KeyError:
        print(f"Column '{column}' not found in DataFrame. Skipping...")
        continue

    # Translate the column values for the first 5 rows
    translated_values = batch_translate_text(column_values)

    # Check if the length of translated_values matches the length of df_subset
    if len(translated_values) != len(df_subset):
        # If not, pad translated_values with empty strings to match the length
        translated_values.extend([''] * (len(df_subset) - len(translated_values)))
        print(f"Warning: Length mismatch for column '{column}'. Padding with empty strings.")

    # Overwrite the original DataFrame rows with the translated values
    df.loc[df.index[:5], column] = translated_values

# Step 4: Save the result back to a CSV file (or overwrite the original if needed)
output_file_path = '/content/translated_with_original.csv'
df.to_csv(output_file_path, index=False)

print(f"Translation of headers and first 5 rows completed and saved to '{output_file_path}'.")

import pandas as pd

# Load the previously translated CSV file with specified data types
# Verify the file path, ensure that 'translated_with_original.csv' exists in '/content/'
file_path = '/content/translated_with_original.csv'  # Replace with the actual file path if it's different

# Specifying dtype to avoid mixed types warnings
dtype_mapping = {
    'VIN': str,
    'Name': str,
    'ID_Number': str,
    'Gender': str,
    'Mobile_Phone': str,
    'Email': str,
    'Province': str,
    'City': str,
    'Address': str,  # Assuming 'Address' is the original column name
    'Postal_Code': str,
    'Monthly_Salary': str,
    'Marital_Status': str,
    'Education': str,
    'Brand': str,
    'Vehicle_Series': str,
    'Vehicle_Model': str,
    'Configuration': str,
    'Color': str,
    'Engine_Number': str
}

# Load the DataFrame with the specified dtype
df = pd.read_csv(file_path, dtype=dtype_mapping)

# Display the original DataFrame to check the structure
print("Original DataFrame:")
print(df.head())

# Check if the expected columns exist, if not, find possible matches
expected_columns = ['Address', 'City', 'Province', 'Postal_Code']
for col in expected_columns:
    if col not in df.columns:
        print(f"Warning: Column '{col}' not found in DataFrame. Trying to find a match...")
        # Find potential matches based on partial string match (case-insensitive)
        possible_matches = [c for c in df.columns if col.lower() in c.lower()]
        if possible_matches:
            # Rename the matched column to the expected name
            df.rename(columns={possible_matches[0]: col}, inplace=True)
            print(f"Column '{possible_matches[0]}' renamed to '{col}'")
        else:
            # Handle the case where no match is found
            print(f"Could not find a suitable replacement for column '{col}'. This might cause issues later.")
    else:
        # Convert potential float values to string before applying .join
        df[col] = df[col].astype(str) 

# Combine 'Address', 'City', 'Province', 'Postal_Code' into one column 'Full_Address'
# Only if all expected columns are present
if all(col in df.columns for col in expected_columns):
    df['Full_Address'] = df[['Address', 'City', 'Province', 'Postal_Code']].agg(', '.join, axis=1)
else:
    print("Warning: Could not create 'Full_Address' column because some expected columns are missing.")
    # If 'Full_Address' cannot be created, you might want to skip the steps that depend on it
    # or provide an alternative way to proceed


# List of columns to remove
columns_to_remove = [
    'ID_Number',
    'Gender',
    'Address',
    'City',
    'Province',
    'Postal_Code',
    'Date_of_Birth',  # Ensure this matches the translated name
    'Industry',       # Ensure this matches the translated name
    'Monthly_Salary',
    'Marital_Status',
    'Education',
    'Configuration',
    'Color',
    'unnamed_21'      # Trying to remove
]

# Check for 'Unnamed: 21' or similar variations and add them to the list
columns_to_remove += [col for col in df.columns if 'Unnamed' in col]

# Drop only columns that exist in the DataFrame
df_cleaned = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

# Remove duplicate rows
df_cleaned = df_cleaned.drop_duplicates()

# Display the cleaned DataFrame to verify removal and combination
# Check if 'Full_Address' exists before trying to access it
if 'Full_Address' in df_cleaned.columns:
    print("\nCleaned DataFrame with combined address and duplicates removed:")
    print(df_cleaned[['Full_Address']].head())
else:
    print("\nWarning: 'Full_Address' column not found in cleaned DataFrame. Skipping display.")

# Save the cleaned DataFrame to a new CSV file as nationwide_pan1
output_file_path = '/content/760k-Car-Owners-Nationwide-China-csv-2020_cleaned.csv'
df_cleaned.to_csv(output_file_path, index=False)

# Verify the columns in the cleaned DataFrame
print("\nColumns in cleaned DataFrame:")
print(df_cleaned.columns)

import pandas as pd
import re

# Function to clean special characters from all string columns
def clean_special_characters(df):
    # Apply the cleaning function to all string columns
    return df.applymap(lambda x: re.sub(r'[^a-zA-Z0-9\s@.-]', '', str(x)) if isinstance(x, str) else x)

# Load the CSV file into a DataFrame
csv_file_path = '/content/translated_with_original.csv'
df = pd.read_csv(csv_file_path)

# Rename 'Birthday' to 'Date_of_birth'
df.rename(columns={'Birthday': 'Date_of_birth'}, inplace=True)

# Clean special characters from the entire DataFrame
df = clean_special_characters(df)

# Separate rows with missing values into a new DataFrame
missing_values_df = df[df.isnull().any(axis=1)]

# Save the missing values into a separate CSV file
missing_values_file = '/content/missing_values.csv'
missing_values_df.to_csv(missing_values_file, index=False)
print(f"Missing values saved to '{missing_values_file}'.")

# Remove rows with missing values from the original DataFrame
df.dropna(inplace=True)

# Overwrite the original file with the cleaned data
df.to_csv(csv_file_path, index=False)
print(f"Cleaned data without missing values saved to '{csv_file_path}'.")

# Print the first few rows of the cleaned DataFrame
print(df.head())
