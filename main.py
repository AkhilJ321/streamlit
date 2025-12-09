import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from utils import (
    load_data, get_unique_values, calculate_correlation_matrix,
    filter_data, get_top_producing_districts, get_time_series_data,
    get_multi_metric_time_series, get_crop_wise_production,
    get_yield_by_district, get_yield_by_state, prepare_scatter_data,
    get_state_coordinates, get_district_yield_table, load_geojson,
    prepare_state_data_for_map
)

st.set_page_config(layout="wide")

df = load_data("data.csv")

state = get_unique_values(df, 'State')
district = get_unique_values(df, 'District')
crop = get_unique_values(df, 'Crop')
season = get_unique_values(df, 'Season')
year = get_unique_values(df, 'Year')

with st.sidebar:
    selected = option_menu(
        "Dashboard",
        ["Dashboard", "Map View"],
        default_index=0
    )

if selected == "Dashboard":
    st.markdown("<h1 style='text-align:center;'>Crop Production & Yield Dashboard</h1>", unsafe_allow_html=True)

    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([1,1,1,1,1])

    with filter_col1:
        stateOptions = st.multiselect("State (multi-select)", state, default=None)
    with filter_col2:
        districtOptions = st.multiselect("District (multi-select)", district, default=None)
    with filter_col3:
        cropOptions = st.multiselect("Crop (multi-select)", crop, default=None)
    with filter_col4:
        seasonOptions = st.multiselect("Season (multi-select)", season, default=None)
    with filter_col5:
        years = st.multiselect("Year Selector (multi-select)", year, default=None)

    filtered_df = filter_data(df, stateOptions, districtOptions, cropOptions, seasonOptions, years)

    left, right = st.columns([1,1])

    with left:
        st.markdown("### Correlation Matrix")
        matrix = calculate_correlation_matrix(df, ['Area','Production','Yield'])
        fig_corr, ax_corr = plt.subplots(figsize=(7, 5))
        sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".3f", linewidths=.5, ax=ax_corr)
        ax_corr.set_title('Correlation Matrix')
        st.pyplot(fig_corr)
        plt.close()

        st.markdown("### Top Producing Districts")
        top_districts = get_top_producing_districts(filtered_df, top_n=10)
        fig_top, ax_top = plt.subplots(figsize=(7, 4))
        top_districts.plot(kind='bar', ax=ax_top, color='teal')
        ax_top.set_title("Top Producing Districts")
        ax_top.set_xlabel("District")
        ax_top.set_ylabel("Total Production")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig_top)
        plt.close()

        st.markdown("### Yield vs Production Area")
        scatter_data = prepare_scatter_data(df)
        if len(scatter_data) > 0:
            fig_scatter, ax_scatter = plt.subplots(figsize=(7, 5))
            sizes = scatter_data['Production'] / scatter_data['Production'].max() * 500
            scatter = ax_scatter.scatter(
                scatter_data['Area'],
                scatter_data['Yield'],
                s=sizes,
                alpha=0.6,
                c=scatter_data['Yield'],
                cmap='viridis',
                edgecolors='black',
                linewidth=0.5
            )
            ax_scatter.set_xlabel('Area (Hectares)')
            ax_scatter.set_ylabel('Yield (Tonnes/Hectare)')
            ax_scatter.set_title('Yield vs Production Area')
            plt.colorbar(scatter, ax=ax_scatter, label='Yield')
            st.pyplot(fig_scatter)
            plt.close()
        else:
            st.info('No data available')

    with right:
        st.markdown("### Time Series")
        time_series_data = get_multi_metric_time_series(df)
        
        fig_ts, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
        
        ax1.plot(time_series_data.index, time_series_data['Area'], marker='o', color='blue', linewidth=2)
        ax1.set_ylabel('Area', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(time_series_data.index, time_series_data['Production'], marker='s', color='green', linewidth=2)
        ax2.set_ylabel('Production', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(time_series_data.index, time_series_data['Yield'], marker='^', color='red', linewidth=2)
        ax3.set_ylabel('Yield', color='red')
        ax3.set_xlabel('Year')
        ax3.tick_params(axis='y', labelcolor='red')
        ax3.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        fig_ts.suptitle('Time Series Analysis', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_ts)
        plt.close()

        st.markdown("### Yield")
        yield_table = get_district_yield_table(filtered_df)
        st.dataframe(
            yield_table.style.background_gradient(cmap='RdYlGn', subset=['Yield']),
            use_container_width=True,
            height=400
        )

        st.markdown("### Crop-wise Production")
        crop_production = get_crop_wise_production(filtered_df, cropOptions if cropOptions else None)
        fig_crop = go.Figure()
        for crop_name in crop_production.columns:
            fig_crop.add_trace(go.Scatter(
                x=crop_production.index,
                y=crop_production[crop_name],
                mode='lines+markers',
                name=crop_name
            ))
        fig_crop.update_layout(
            title='Crop-wise Production Over Time',
            xaxis_title='Year',
            yaxis_title='Production',
            hovermode='x unified'
        )
        st.plotly_chart(fig_crop, use_container_width=True)

elif selected == "Map View":
    st.markdown("<h1 style='text-align:center;'>Map View</h1>", unsafe_allow_html=True)
    
    st.markdown("### Filters")
    map_col1, map_col2, map_col3 = st.columns([1, 1, 1])
    
    with map_col1:
        map_states = st.multiselect("Select States", state, default=None, key="map_states")
    with map_col2:
        map_districts = st.multiselect("Select Districts", district, default=None, key="map_districts")
    with map_col3:
        metric_choice = st.selectbox("Select Metric", ["Yield", "Production", "Area"], index=0)
    
    filtered_map_df = filter_data(df, map_states, map_districts, None, None, None)
    
    state_data = prepare_state_data_for_map(filtered_map_df)
    
    india_geo = load_geojson('india_state_geo.json')
    
    state_name_map = {}
    for feature in india_geo['features']:
        geo_name = feature['properties']['NAME_1']
        if 'Andaman' in geo_name:
            state_name_map['Andaman and Nicobar Islands'] = geo_name
        elif 'Arunachal' in geo_name:
            state_name_map['Arunachal Pradesh'] = geo_name
        elif 'Dadara' in geo_name or 'Dadra' in geo_name:
            state_name_map['Dadra and Nagar Haveli'] = geo_name
        elif 'Jammu' in geo_name:
            state_name_map['Jammu and Kashmir'] = geo_name
        else:
            for csv_state in state_data['State'].unique():
                if csv_state.lower().replace(' ', '') in geo_name.lower().replace(' ', ''):
                    state_name_map[csv_state] = geo_name
                    break
    
    state_data['GeoName'] = state_data['State'].map(state_name_map)
    
    fig_map = px.choropleth(
        state_data,
        geojson=india_geo,
        locations='GeoName',
        featureidkey='properties.NAME_1',
        color=metric_choice,
        hover_name='State',
        hover_data={
            'GeoName': False,
            'Yield': ':.3f',
            'Production': ':,.0f',
            'Area': ':,.0f'
        },
        color_continuous_scale='YlGnBu',
        title=f'{metric_choice} by State'
    )
    
    fig_map.update_geos(
        fitbounds="locations",
        visible=False
    )
    
    fig_map.update_layout(
        height=700,
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("### State-wise Data Table")
    display_data = state_data[['State', 'Yield', 'Production', 'Area']].sort_values(metric_choice, ascending=False)
    st.dataframe(
        display_data.style.background_gradient(cmap='YlGnBu', subset=[metric_choice]),
        use_container_width=True,
        height=400
    )
