import pandas as pd
from pathlib import Path

# Load the rough house price dataset
file_path = Path(__file__).with_name("House_Price_Prediction_Extra_Rough.csv")
df = pd.read_csv(file_path)

# Take approximate house details from the user
print("\nEnter House Details (approximate values are also accepted):")

def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Please enter a value greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

user_floors = get_positive_number("Enter number of floors: ")
user_bedrooms = get_positive_number("Enter number of bedrooms: ")

while True:
    try:
        user_year = int(input("Enter year built: "))
        if 1800 <= user_year <= 2100:
            break
        print("Please enter a year between 1800 and 2100.")
    except ValueError:
        print("Please enter a valid year.")



print("Original Dataset:")
print(df.head())

# 1. Remove duplicate rows and duplicate house IDs
df = df.drop_duplicates()
if "Id" in df.columns:
    df = df.drop_duplicates(subset=["Id"], keep="first")

# 2. Clean text columns (remove extra spaces)
text_columns = ["Location", "Condition", "Garage"]
for column in text_columns:
    if column in df.columns:
        df[column] = df[column].astype("string").str.strip()

# 3. Standardize text values
if "Location" in df.columns:
    df["Location"] = df["Location"].str.title()

if "Condition" in df.columns:
    df["Condition"] = df["Condition"].str.title()

if "Garage" in df.columns:
    df["Garage"] = df["Garage"].str.lower().map({
        "yes": "Yes",
        "no": "No"
    })

# 4. Convert numeric columns into numbers
numeric_columns = [
    "Area", "Bedrooms", "Bathrooms", "Floors", "YearBuilt", "Price"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# 5. Replace missing numeric values with the column median
for column in numeric_columns:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())

# 6. Replace missing text values with the most frequent value
for column in text_columns:
    if column in df.columns and df[column].notna().any():
        mode_value = df[column].mode()
        if not mode_value.empty:
            df[column] = df[column].fillna(mode_value[0])

# 7. Calculate average area and average number of floors
average_area = df["Area"].mean()
average_floors = df["Floors"].mean()

print("\nData Cleaning Completed!")
print("Cleaned Dataset:")
print(df.head())

print("\nAverage Area:", round(average_area, 2))
print("Average Number of Floors:", round(average_floors, 2))


# 8. Display the details entered by the user
print("\nYour Entered House Details:")
print("Number of Floors:", user_floors)
print("Number of Bedrooms:", user_bedrooms)
print("Year Built:", user_year)

# 8. Save the cleaned dataset
output_path = Path(__file__).with_name("House_Price_Cleaned.csv")
df.to_csv(output_path, index=False)

print("\nCleaned file saved as:", output_path.name)
