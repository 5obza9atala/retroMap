import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import re

# Prevent font caching delays
plt.rcParams['font.family'] = 'sans-serif'

# Set user agent and reliable mirror
ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Public/1.0'}
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'
ox.settings.timeout = 90

st.set_page_config(page_title="Retro Map Generator", page_icon="🗺️")
st.title("🗺️ Custom Retro Map Generator")
st.write("Generate and download retro-styled vector maps for any location in the world.")

# Input fields
location_input = st.text_input(
    "Enter City Name or Coordinates (lat, lon):", 
    value="Chefchaouen, Morocco"
)

map_radius = st.slider(
    "Map Radius (Meters):", 
    min_value=50, 
    max_value=1200, 
    value=200, 
    step=50,
    help="Keep under 500m on cloud hosting for fastest render times."
)

def parse_location(raw_input: str):
    """Detects if input is GPS coordinates or a city string."""
    cleaned = raw_input.strip().strip("()[]")
    coord_match = re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", cleaned)
    if coord_match:
        lat, lon = map(float, cleaned.split(","))
        return (lat, lon)
    return raw_input.strip()

if st.button("Generate Map", type="primary"):
    with st.spinner("Downloading spatial geometry and drawing map..."):
        try:
            target_location = parse_location(location_input)
            
            # Plot the map with bounded canvas dimensions
            plot = prettymaps.plot(
                target_location, 
                radius=map_radius, 
                preset='heerhugowaard',
                figsize=(10, 10)
            )
            
            fig = plt.gcf()
            
            # Save into an in-memory buffer
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300)
            buf.seek(0)
            img_bytes = buf.getvalue()
            
            # Display image in Streamlit
            st.image(img_bytes, caption=f"Generated Map: {location_input}", use_container_width=True)
            
            # Download Button
            safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', location_input).lower()
            st.download_button(
                label="📥 Download Map (.png)",
                data=img_bytes,
                file_name=f"{safe_filename}_retro_map.png",
                mime="image/png"
            )
            
            plt.close(fig)
            st.success("Map generated successfully!")
            
        except Exception as e:
            st.error(f"Could not generate map for '{location_input}'. Error: {e}")
