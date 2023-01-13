
import streamlit as st
import folium
import pandas as pd 
import streamlit_pandas as sp
from streamlit_folium import st_folium

st.title("Map Demo Test")
st.write("The map below is supposed to display a potential implementation of cartographic visualizations for an example data set.")
st.sidebar.header("Select Options")


@st.cache(allow_output_mutation=True) ## only "for-the-time-being"-solution as individual request are to be made with the APIs --> reload needed!
def load_data():
    df = pd.read_csv(file)
    return df

file = "test_data.csv"
df = load_data()


multiselect_options = {
    "Lithology/Mineral" : "multiselect",
    "Sample" : "multiselect",
    "Location Type" : "multiselect",
    "Data Package" : "multiselect"    
}


interactive_widgets = sp.create_widgets(df, multiselect_options)
widget_filter = sp.filter_df(df, interactive_widgets)
st.write(widget_filter)


world_map = folium.Map(
    zoom_start = 4,
    location = [-25.0000, 140.0000])

df_2 = widget_filter.dropna(subset=['Longitude'])
df_2 = widget_filter.dropna(subset=['Latitude'])

for _, site in df_2.iterrows():
    folium.Marker(
        location = [site['Latitude'], site['Longitude']], #also einfach der Name der jeweiligen Spalten/Columns
        popup = site['Lithology/Mineral'],
        tooltip = site['Lithology/Mineral'],
    ).add_to(world_map)  

st_world_map = st_folium(world_map, width=700, height=450) 
