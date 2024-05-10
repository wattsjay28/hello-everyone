import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import warnings


# Load the dataset into a DataFrame
data = pd.read_csv("vehicles_us.csv")

# Remove Warnings
warnings.filterwarnings('ignore')

# Define columns to fill missing values for and their respective groupby columns and fill methods
columns_to_fill = {
    'cylinders': {'groupby_cols': ['model', 'model_year'], 'fill_method': 'median'},
    'price': {'groupby_cols': ['model', 'model_year'], 'fill_method': 'median'},
    'odometer': {'groupby_cols': ['model', 'model_year'], 'fill_method': 'median'},
    'condition': {'groupby_cols': ['model'], 'fill_method': 'mode'},
    'fuel': {'groupby_cols': ['model'], 'fill_method': 'mode'},
    'transmission': {'groupby_cols': ['model'], 'fill_method': 'mode'},
    'paint_color': {'groupby_cols': ['model'], 'fill_method': 'mode'},
    'type': {'groupby_cols': ['model'], 'fill_method': 'mode'},
    'is_4wd': {'groupby_cols': ['model'], 'fill_method': 'median'}
}

# Apply fillna with group-specific statistics for each column
for column, config in columns_to_fill.items():
    groupby_cols = config['groupby_cols']
    fill_method = config['fill_method']
    if fill_method == 'median':
        fill_value = data.groupby(groupby_cols)[column].transform(lambda x: x.fillna(x.median()))
    elif fill_method == 'mode':
        fill_value = data.groupby(groupby_cols)[column].transform(lambda x: x.fillna(x.mode()[0]))  # mode returns a Series, so we use [0] to get the first mode
    data[column] = fill_value


# List of car manufacturers
Manufacturers = [
    'BMW', 'Honda', 'Kia', 'GMC', 'Jeep', 'Chevrolet', 'Toyota', 'Subaru',
    'Nissan', 'Ford', 'Hyundai', 'Cadillac', 'Buick', 'Ram', 'Dodge',
    'Acura', 'Chrysler', 'Volkswagen', 'Mercedes-Benz'
]

# Function to extract manufacturer name from model
def extract_Manufacturer(model):
    for Manufacturer in Manufacturers:
        if Manufacturer.lower() in model.lower():
            return Manufacturer
    return None

# Create a new column "Manufacturer" and extract manufacturer names
data['Manufacturer'] = data['model'].apply(extract_Manufacturer)

# Remove manufacturer names from "model" column
data['model'] = data['model'].apply(lambda x: ' '.join(word for word in x.split() if word.lower() not in Manufacturers))

# Group by Manufacturer and Vehicle Type, and count the number of vehicles for each combination
Manufacturer_type_counts = data.groupby(['Manufacturer', 'type']).size().unstack(fill_value=0)


# List of words to remove from the "model" column
words_to_remove = ['bmw', 'honda', 'kia', 'gmc', 'jeep', 'chevrolet', 'toyota', 'subaru',
                   'nissan', 'ford', 'hyundai', 'cadillac', 'buick', 'ram', 'dodge',
                   'acura', 'chrysler', 'volkswagen', 'mercedes-benz']

# Remove specified words from the "model" column
data['model'] = data['model'].apply(lambda x: ' '.join(word for word in x.split() if word.lower() not in words_to_remove))

