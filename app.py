import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib.pyplot as plt

# Swapped to the primary global OpenStreetMap server
ox.settings.overpass_endpoint = 'https://overpass-api.de/api/interpreter'
ox.settings.timeout = 180 

st.title("🗺️ Custom Retro Map Generator")

location = st.text_input("Enter a City or Coordinates:", "Chefchaouen, Morocco")
map_radius = st.slider("Map Radius (Meters) - Keep under 500 for faster loading:", 100, 1500, 300)

if st.button("Generate Map"):
    with st.spinner("Drawing map... smaller radiuses load much faster!"):
        try:
            plot = prettymaps.plot(location, radius=map_radius, preset='heerhugowaard')
            
            fig = plt.gcf()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
