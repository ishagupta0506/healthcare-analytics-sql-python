# Hospital Patient Analytics — Data Cleaning

import pandas as pd

# Load dataset
df = pd.read_csv("../data/healthcare_dataset.csv")

# Basic info
print("Original Shape:", df.shape)

# Handle missing values
df = df.dropna(subset=['Date of Admission', 'Discharge Date'])
df['Billing Amount'] = df['Billing Amount'].fillna(df['Billing Amount'].median())

# Standardize text
df['Name'] = df['Name'].str.title()

# Convert date columns
df['Date of Admission'] = pd.to_datetime(
    df['Date of Admission'],
    dayfirst=True,
    errors='coerce'
)

df['Discharge Date'] = pd.to_datetime(
    df['Discharge Date'],
    dayfirst=True,
    errors='coerce'
)

# Feature Engineering: Length of Stay
df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days

# Round billing
df['Billing Amount'] = df['Billing Amount'].round(2)

# Create Age Groups
df['Age Group'] = pd.cut(
    df['Age'],
    bins=[0, 18, 35, 60, 100],
    labels=['0-18', '19-35', '36-60', '60+']
)

# Extract time-based features
df['Admission Year'] = df['Date of Admission'].dt.year
df['Admission Month'] = df['Date of Admission'].dt.month
df['Day of Week'] = df['Date of Admission'].dt.day_name()

# Final check
print("Cleaned Shape:", df.shape)

df.columns = [
    col.strip()
       .replace(" ", "_")
       .replace("-", "_")
    for col in df.columns
]

# Save cleaned dataset
df.to_csv("../data/hospital_cleaned.csv", index=False)
print("Cleaned file saved.")
