
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# Create a dictionary of base maps with their names and tiles
base_maps = {
    "OpenStreetMap": folium.TileLayer("cartodbpositron"),
    "Stamen Terrain": folium.TileLayer("Stamen Terrain"),
    "Stamen Toner": folium.TileLayer("Stamen Toner"),
    "Stamen Watercolor": folium.TileLayer("Stamen Watercolor"),
}
   
st.title("Map Demo Test")
st.write("The map below is supposed to display a potential implementation of cartographic visualizations for an example data set.")
st.sidebar.header("Select Options")

@st.cache_data() 
def load_data():
    df = pd.read_csv(file)
    return df

file = "cleaned_data.csv"
df = load_data()
df.rename(columns={'Lithology/Mineral' : 'Lithology_Mineral'}, inplace=True)

form1 = st.sidebar.form(key="Options")
location_type = form1.multiselect(
    "Choose the location type:",
    options =df["Location Type"].unique()
)

material = form1.multiselect(
    "Choose the lithology/mineral",
    options = df["Lithology_Mineral"].unique()
)

sample = form1.multiselect(
    "Choose the sample",
    options = df["Sample"].unique()
)

data_package = form1.multiselect(
    "Choose the data package",
    options = df["Data Package"].unique()
)

location_type_str = '|'.join(location_type)
material_str = '|'.join(material)
sample_str = '|'.join(sample)
data_package_str = '|'.join(data_package)

# Filter dataframe using str.contains
df_selection = df[df['Location Type'].str.contains(location_type_str) & 
                  df['Lithology_Mineral'].str.contains(material_str) & 
                  df['Sample'].str.contains(sample_str) & 
                  df['Data Package'].str.contains(data_package_str)]

st.dataframe(df_selection)
form1.form_submit_button("Submit")

df_2 = df_selection.dropna(subset=['Longitude'])
df_2 = df_selection.dropna(subset=['Latitude'])

selected_base_map = st.sidebar.selectbox("Select a base map", list(base_maps.keys()))

world_map = folium.Map(
    zoom_start = 4,
    location = [-25.0000, 140.0000],
    tiles = base_maps[selected_base_map],
)

for _, site in df_2.iterrows():
    folium.Marker(
        location = [site['Latitude'], site['Longitude']], 
        popup = site['Lithology_Mineral'],
        tooltip = site['Lithology_Mineral'],
    ).add_to(world_map)  

st_world_map = st_folium(world_map, width=700, height=450)
