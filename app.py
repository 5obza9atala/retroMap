import streamlit as st
import prettymaps
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import re

# Bypass font cache
plt.rcParams['font.family'] = 'sans-serif'
ox.settings.http_headers = {'User-Agent': 'RetroMapApp_Public/2.0'}
ox.settings.overpass_endpoint = 'https://lz4.overpass-api.de/api/interpreter'
ox.settings.timeout = 90

st.set_page_config(page_title="Pro Map Generator", page_icon="🗺️", layout="wide")
st.title("🗺️ Pro Retro Map Customizer")

# UI Layout: Two neat columns
col1, col2 = st.columns(2)

with col1:
    location_input = st.text_input("Enter City (e.g., Paris, France):", value="London, UK")
    map_radius = st.slider("Map Radius (Meters):", 50, 1000, 300)
    custom_title = st.text_input("Custom Map Title (Optional):", value="LONDON")

with col2:
    map_style = st.selectbox("🎨 Choose a Color Palette:", ["heerhugowaard", "macao", "tijuca", "cbcd"])
    shape_choice = st.radio("📐 Canvas Shape:", ["Circle", "Square"])

# Cache respects the new style and shape choices!
@st.cache_resource(show_spinner=False)
def generate_pro_map(loc, radius, style, shape, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Toggle circular boundary
    is_circle = True if shape == "Circle" else False
    
    prettymaps.plot(
        loc, 
        radius=radius, 
        ax=ax, 
        preset=style,
        circle=is_circle
    )
    
    # Add custom title text to the canvas
    if title:
        ax.set_title(title.upper(), fontsize=24, fontweight='bold', pad=20, color='#2F3737')
        
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

if st.button("🎨 Generate Custom Map", type="primary"):
    with st.spinner("Applying custom styles and rendering canvas..."):
        try:
            img_bytes = generate_pro_map(location_input, map_radius, map_style, shape_choice, custom_title)
            
            st.image(img_bytes, use_container_width=True)
            
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', location_input).lower()
            st.download_button(
                label="📥 Download Artwork (.png)",
                data=img_bytes,
                file_name=f"{safe_name}_{map_style}.png",
                mime="image/png"
            )
            st.success("Masterpiece generated successfully!")
            
        except Exception as e:
            st.error(f"Could not generate map. Error: {e}")
