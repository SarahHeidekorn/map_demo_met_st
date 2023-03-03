
import streamlit as st
import folium
import pandas as pd 
import plotly.express as px
from streamlit_folium import st_folium

st.set_page_config(page_title = "Map Demo", layout = "wide")    
st.title("Map Demo Test")
st.write("The map below is supposed to display a potential implementation of cartographic visualizations for an example data set.")
st.sidebar.header("Select Options")

base_maps = {
    "OpenStreetMap": folium.TileLayer("cartodbpositron"),
    "Terrain": folium.TileLayer("Stamen Terrain"),
    "Toner": folium.TileLayer("Stamen Toner"),
    "Watercolor": folium.TileLayer("Stamen Watercolor"),
}

#@st.cache_data() 
def load_data():
    df = pd.read_csv(file)
    return df

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

world_map = folium.Map(
    zoom_start = 4,
    location = [-25.0000, 140.0000])


for _, site in df_2.iterrows():
    folium.Marker(
        location = [site['Latitude'], site['Longitude']], #also einfach der Name der jeweiligen Spalten/Columns
        popup = site['Lithology_Mineral'],
        tooltip = site['Lithology_Mineral'],
    ).add_to(world_map)  

st_world_map = st_folium(world_map, width=700, height=450) 
