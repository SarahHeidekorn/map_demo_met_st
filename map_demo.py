
import streamlit as st
import folium
import pandas as pd 
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import seaborn as sns


st.set_page_config(page_title = "Map Demo", layout = "wide")    
st.title("Map Demo Test")
st.write("The map below is supposed to display a potential implementation of cartographic visualizations for an example data set.")
st.sidebar.header("Select Options")

#@st.cache_data() 
def load_data():
    df = pd.read_csv(file)
    return df

base_maps = {
    "OpenStreetMap": "cartodbpositron",
    "Stamen Terrain": "Stamen Terrain",
    "Stamen Toner": "Stamen Toner",
    "Stamen Watercolor": "Stamen Watercolor",
}

file = "test_data.csv"
df = load_data()
df.rename(columns={'Lithology/Mineral' : 'Lithology_Mineral'}, inplace=True)

filter_form = st.sidebar.form(key="Options") #create container to optimize functionality

#set filter options
location_type = filter_form.multiselect(
    "Choose the location type:",
    options =df["Location Type"].unique()
)
material = filter_form.multiselect(
    "Choose the lithology/mineral",
    options = df["Lithology_Mineral"].unique()
)
sample = filter_form.multiselect(
    "Choose the sample",
    options = df["Sample"].unique()
)    
data_package = filter_form.multiselect(
    "Choose the data package",
    options = df["Data Package"].unique()
)    
 
location_type_str = '|'.join(location_type)
material_str = '|'.join(material)
sample_str = '|'.join(sample)
data_package_str = '|'.join(data_package)

# filter dataframe using str.contains
df_selection = df[df['Location Type'].str.contains(location_type_str) & 
                  df['Lithology_Mineral'].str.contains(material_str) & 
                  df['Sample'].str.contains(sample_str) & 
                  df['Data Package'].str.contains(data_package_str)]


st.dataframe(df_selection)
filter_form.form_submit_button("Submit")


# construction of the interactive map:
df_2 = df_selection.dropna(subset=['Longitude'])
df_2 = df_selection.dropna(subset=['Latitude'])
df["Lithology_Mineral"].fillna("Unknown", inplace=True)

selected_base_map = st.sidebar.selectbox("Select a base map", list(base_maps.keys()))

world_map = folium.Map(
    zoom_start = 4,
    location = [-25.0000, 140.0000],
    tiles = selected_base_map,
)

unique_lithologies = df['Lithology_Mineral'].unique()
colors = sns.color_palette("husl", len(unique_lithologies))
color_dict = dict(zip(unique_lithologies, colors))
marker_cluster = MarkerCluster().add_to(world_map)

for _, site in df.iterrows():
    if not pd.isna(site['Longitude']) and not pd.isna(site['Latitude']):
        lithology = site['Lithology_Mineral']
        color = color_dict[lithology]
        folium.Marker(
            location=[site['Latitude'], site['Longitude']],
            popup=lithology,
            tooltip=lithology,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)    


st_world_map = st_folium(world_map, width=700, height=450)
