import pandas as pd
import numpy as np
import json

def normalize_production_units(df):
    df = df.copy()
    
    conversion_factors = {
        'Tonnes': 1.0,
        'Bales': 0.17,
        'Nuts': 0.001
    }
    
    df['Production_Normalized'] = df.apply(
        lambda row: row['Production'] * conversion_factors.get(row['Production Units'], 1.0) 
        if pd.notna(row['Production']) and pd.notna(row['Production Units']) 
        else row['Production'],
        axis=1
    )
    
    df['Production'] = df['Production_Normalized']
    df = df.drop(columns=['Production_Normalized'])
    
    return df

def load_data(filepath):
    df = pd.read_csv(filepath)
    df = normalize_production_units(df)
    return df

def get_unique_values(df, column):
    return df[column].unique()

def calculate_correlation_matrix(df, columns):
    subset_data = df[columns]
    return subset_data.corr(method='pearson')

def filter_data(df, state=None, district=None, crop=None, season=None, year=None):
    filtered_df = df.copy()
    
    if state is not None and len(state) > 0:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    if district is not None and len(district) > 0:
        filtered_df = filtered_df[filtered_df['District'].isin(district)]
    if crop is not None and len(crop) > 0:
        filtered_df = filtered_df[filtered_df['Crop'].isin(crop)]
    if season is not None and len(season) > 0:
        filtered_df = filtered_df[filtered_df['Season'].isin(season)]
    if year is not None and len(year) > 0:
        filtered_df = filtered_df[filtered_df['Year'].isin(year)]
    
    return filtered_df

def get_top_producing_districts(df, top_n=10):
    top_districts = (
        df.groupby("District")["Production"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )
    return top_districts

def get_time_series_data(df, metric='Production'):
    time_series = df.groupby('Year')[metric].sum().sort_index()
    return time_series

def get_multi_metric_time_series(df):
    time_series = df.groupby('Year').agg({
        'Area': 'sum',
        'Production': 'sum',
        'Yield': 'mean'
    }).sort_index()
    return time_series

def get_crop_wise_production(df, crops=None):
    if crops is None or len(crops) == 0:
        crops = df['Crop'].unique()[:5]
    
    crop_production = df[df['Crop'].isin(crops)].groupby(['Year', 'Crop'])['Production'].sum().unstack(fill_value=0)
    return crop_production

def get_yield_by_district(df):
    yield_data = df.groupby('District')['Yield'].mean().sort_values(ascending=False)
    return yield_data

def get_district_yield_table(df):
    yield_table = df.groupby('District').agg({
        'Yield': 'mean',
        'Production': 'sum',
        'Area': 'sum'
    }).sort_values('Yield', ascending=False)
    yield_table['Yield'] = yield_table['Yield'].round(3)
    return yield_table

def get_yield_by_state(df):
    yield_data = df.groupby('State')['Yield'].mean().sort_values(ascending=False)
    return yield_data

def prepare_scatter_data(df):
    scatter_data = df.groupby('District').agg({
        'Area': 'sum',
        'Production': 'sum',
        'Yield': 'mean'
    }).reset_index()
    return scatter_data

def get_state_coordinates():
    state_coords = {
        'Andhra Pradesh': (15.9129, 79.7400),
        'Arunachal Pradesh': (28.2180, 94.7278),
        'Assam': (26.2006, 92.9376),
        'Bihar': (25.0961, 85.3131),
        'Chhattisgarh': (21.2787, 81.8661),
        'Goa': (15.2993, 74.1240),
        'Gujarat': (22.2587, 71.1924),
        'Haryana': (29.0588, 76.0856),
        'Himachal Pradesh': (31.1048, 77.1734),
        'Jharkhand': (23.6102, 85.2799),
        'Karnataka': (15.3173, 75.7139),
        'Kerala': (10.8505, 76.2711),
        'Madhya Pradesh': (22.9734, 78.6569),
        'Maharashtra': (19.7515, 75.7139),
        'Manipur': (24.6637, 93.9063),
        'Meghalaya': (25.4670, 91.3662),
        'Mizoram': (23.1645, 92.9376),
        'Nagaland': (26.1584, 94.5624),
        'Odisha': (20.9517, 85.0985),
        'Punjab': (31.1471, 75.3412),
        'Rajasthan': (27.0238, 74.2179),
        'Sikkim': (27.5330, 88.5122),
        'Tamil Nadu': (11.1271, 78.6569),
        'Telangana': (18.1124, 79.0193),
        'Tripura': (23.9408, 91.9882),
        'Uttar Pradesh': (26.8467, 80.9462),
        'Uttarakhand': (30.0668, 79.0193),
        'West Bengal': (22.9868, 87.8550),
        'Andaman and Nicobar Islands': (11.7401, 92.6586),
        'Chandigarh': (30.7333, 76.7794),
        'Dadra and Nagar Haveli': (20.1809, 73.0169),
        'Daman and Diu': (20.4283, 72.8397),
        'Delhi': (28.7041, 77.1025),
        'Jammu and Kashmir': (33.7782, 76.5762),
        'Lakshadweep': (10.5667, 72.6417),
        'Puducherry': (11.9416, 79.8083)
    }
    return state_coords

def load_geojson(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def prepare_state_data_for_map(df):
    state_data = df.groupby('State').agg({
        'Yield': 'mean',
        'Production': 'sum',
        'Area': 'sum'
    }).reset_index()
    
    state_name_mapping = {
        'Andaman and Nicobar': 'Andaman and Nicobar Islands',
        'Arunachal Prades': 'Arunachal Pradesh',
        'Dadara and Nagar': 'Dadra and Nagar Haveli',
        'Daman and Diu': 'Daman and Diu',
        'Jammu and Kashm': 'Jammu and Kashmir',
        'NCT of Delhi': 'Delhi',
        'Pondicherry': 'Puducherry',
        'Telangana': 'Telangana',
        'Chhattisgarh': 'Chhattisgarh'
    }
    
    return state_data
