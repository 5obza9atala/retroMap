import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Bypass the font cache loop
plt.rcParams['font.family'] = 'sans-serif'

ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Morocco/1.0'}
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'

st.title("🗺️ Custom Retro Map Generator")
st.info("Canvas limits strictly enforced to prevent 5-billion-pixel explosions!")

map_radius = st.slider("Map Radius (Meters):", 50, 1500, 200)

if st.button("Generate Map"):
    with st.spinner("Drawing bounded retro map..."):
        try:
            plot = prettymaps.plot(
                (35.1686, -5.2628), 
                radius=map_radius, 
                preset='heerhugowaard',
                figsize=(10, 10) 
            )
            
            fig = plt.gcf()
            image_path = "generated_map.png"
            
            # THE FIX: Removed bbox_inches='tight' to stop the massive expansion!
            fig.savefig(image_path, dpi=300)
            st.image(image_path)
            
            plt.close(fig)
            st.success("Map generated successfully!")
            
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
