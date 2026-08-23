import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib.pyplot as plt

# The reliable global mirror
ox.settings.overpass_endpoint = 'https://overpass.nchc.org.tw/api/interpreter'
ox.settings.timeout = 180 # Give the server more time to respond

st.title("🗺️ Custom Retro Map Generator")

# Interactive Widgets
location = st.text_input("Enter a City or Coordinates:", "Chefchaouen, Morocco")
# Add a slider so you can control how heavy the map is!
map_radius = st.slider("Map Radius (Meters) - Keep under 500 for faster loading:", 100, 1500, 300)

if st.button("Generate Map"):
    with st.spinner("Drawing map... smaller radiuses load much faster!"):
        try:
            # Use the new slider variable
            plot = prettymaps.plot(location, radius=map_radius, preset='heerhugowaard')
            
            fig = plt.gcf()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
