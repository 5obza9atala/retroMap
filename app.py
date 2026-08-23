import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Morocco/1.0'}
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'

st.title("🗺️ Custom Retro Map Generator")
st.info("Canvas strictly locked to prevent memory overload.")

if st.button("Generate Minimalist Map"):
    with st.spinner("Drawing locked-size map..."):
        try:
            clean_style = {
                'background': {'fc': '#E8DCC4', 'ec': '#C2B29A'},
                'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0},
                'building': {'palette': ['#43C6DB', '#1569C7', '#2B547E'], 'ec': '#2F3737', 'lw': 0.5}
            }

            # THE FIX: Explicitly lock the figsize to (10, 10) so it cannot inflate!
            plot = prettymaps.plot(
                (35.1686, -5.2628), 
                radius=150,
                style=clean_style,
                figsize=(10, 10) 
            )
            
            fig = plt.gcf()
            image_path = "generated_map.png"
            
            fig.savefig(image_path, dpi=150, bbox_inches='tight')
            st.image(image_path)
            
            plt.close(fig)
            st.success("Map generated successfully!")
            
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
