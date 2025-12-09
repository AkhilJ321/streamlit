# Crop Production & Yield Dashboard

A simple and interactive dashboard to visualize crop production, yield, and area data across India.

## What This Dashboard Does

This dashboard helps you explore agricultural data with:

- **Charts and graphs** showing crop production trends over time
- **Interactive maps** displaying yield across Indian states
- **Filters** to focus on specific states, districts, crops, seasons, and years
- **Tables** with color-coded data for easy comparison

## Tools Used

- **Python** - Programming language
- **Streamlit** - Web dashboard framework
- **Pandas** - Data processing
- **Matplotlib & Seaborn** - Chart creation
- **Plotly** - Interactive visualizations and maps

## Setup Instructions

### 1. Install Python

Make sure you have Python 3.7 or higher installed on your computer.

### 2. Create Virtual Environment

Open your terminal and navigate to the project folder, then run:

```bash
python -m venv env
```

### 3. Activate Virtual Environment

```bash
source env/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Run the Dashboard

```bash
streamlit run main.py
```

The dashboard will open automatically in your web browser at `http://localhost:8501`

## How to Use

### Dashboard View

1. **Select Filters** - Use the dropdown menus at the top to filter by:

   - State
   - District
   - Crop type
   - Season
   - Year

2. **View Charts**:
   - **Correlation Matrix** - Shows relationships between Area, Production, and Yield
   - **Top Producing Districts** - Bar chart of highest producing districts
   - **Yield vs Production Area** - Scatter plot showing the relationship
   - **Time Series** - Trends of Area, Production, and Yield over years
   - **Yield Table** - District-wise yield with color coding
   - **Crop-wise Production** - Production trends for different crops

### Map View

1. Click **Map View** in the sidebar
2. Use filters to select specific states or districts
3. Choose a metric (Yield, Production, or Area) from the dropdown
4. View the color-coded map of India
5. Scroll down to see the data table

## Files in This Project

- `main.py` - Main dashboard application
- `utils.py` - Helper functions for data processing
- `data.csv` - Agricultural data (Area, Production, Yield)
- `india_state_geo.json` - Map boundaries for Indian states
- `requirements.txt` - List of required Python packages

## Features

### Data Processing

- Automatically converts different production units (Tonnes, Bales, Nuts) to a standard unit
- Filters data based on your selections
- Calculates correlations and aggregations

### Visualizations

- **6 different chart types** in Dashboard view
- **Interactive choropleth map** in Map view
- **Color-coded tables** for easy data comparison
- All charts update automatically when you change filters
