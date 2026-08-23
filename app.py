import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib.pyplot as plt

# Swapped to a secondary main global mirror
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'

st.title("🗺️ Custom Retro Map Generator")

location = st.text_input("Enter a City or Coordinates:", "Chefchaouen, Morocco")

if st.button("Generate Map"):
    with st.spinner("Drawing map... this may take a minute!"):
        try:
            plot = prettymaps.plot(location, radius=800, preset='heerhugowaard')
            
            fig = plt.gcf()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")