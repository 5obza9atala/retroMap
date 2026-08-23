import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib.pyplot as plt

# 1. Give your app a name so the server doesn't block it as a bot
ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Morocco/1.0'}

# 2. Switch back to the ultra-fast French/German hybrid mirror
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'
ox.settings.timeout = 90 

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
