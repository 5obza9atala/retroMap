import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Bypass the infinite font-search loop!
plt.rcParams['font.family'] = 'sans-serif'

ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Morocco/1.0'}
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'
ox.settings.timeout = 90 

st.title("🗺️ Custom Retro Map Generator")

location = st.text_input("Enter a City or Coordinates:", "Chefchaouen, Morocco")
map_radius = st.slider("Map Radius (Meters):", 50, 1500, 100)

if st.button("Generate Map"):
    with st.spinner("Drawing map..."):
        try:
            plot = prettymaps.plot(location, radius=map_radius, preset='heerhugowaard')
            fig = plt.gcf()
            
            image_path = "generated_map.png"
            fig.savefig(image_path, dpi=300, bbox_inches='tight')
            st.image(image_path)
            
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
