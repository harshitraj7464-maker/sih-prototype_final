import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
from streamlit_folium import st_folium

# 1. Page Configuration
st.set_page_config(
    page_title="SIH26001 - GIS Risk Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌋 SIH26001: Integrated GIS Landslide Risk Dashboard")
st.caption("Automated Zone-Wise Heatmaps & Critical Infrastructure Prioritization Engine")

# --- 2. Advanced Mock Data Systems ---
landslide_sensors = [
    {"name": "Joshimath Slope A", "coords": [30.5524, 79.5663], "risk": "High", "intensity": 1.0, "color": "red"},
    {"name": "Joshimath Slope B", "coords": [30.5590, 79.5720], "risk": "High", "intensity": 0.9, "color": "red"},
    {"name": "Rudraprayag Valley", "coords": [30.2844, 78.9811], "risk": "Medium", "intensity": 0.6, "color": "orange"},
    {"name": "Karnaprayag NH Intersection", "coords": [30.2604, 79.2190], "risk": "High", "intensity": 0.95, "color": "red"},
    {"name": "Uttarkashi Route", "coords": [30.7268, 78.4354], "risk": "Low", "intensity": 0.2, "color": "green"}
]

infrastructure_assets = [
    {"name": "National Highway 7 (NH7)", "type": "Road", "coords": [30.5500, 79.5600], "status": "Critical Priority", "icon": "road", "color": "red", "desc": "Main lifeline route; adjacent to active subsidence zone."},
    {"name": "Helang-Marwari Bypass", "type": "Road", "coords": [30.5310, 79.5100], "status": "Watch List", "icon": "road", "color": "orange", "desc": "Alternative transport corridor showing minor rockfall signs."},
    {"name": "Chhatwapal Village", "type": "Village", "coords": [30.5610, 79.5800], "status": "Critical Priority", "icon": "home", "color": "red", "desc": "Population 450+; high density of structural wall cracks detected."},
    {"name": "Srinagar Garhwal Settlement", "type": "Village", "coords": [30.2220, 78.7800], "status": "Safe / Stable", "icon": "home", "color": "green", "desc": "Low slope gradient; stable ground monitoring baselines."},
    {"name": "Tapovan Hydroelectric Dam", "type": "Critical Infrastructure", "coords": [30.4950, 79.6280], "status": "High Priority", "icon": "flash", "color": "darkred", "desc": "Strategic asset down-valley from active glacial/debris zones."},
    {"name": "District General Hospital", "type": "Critical Infrastructure", "coords": [30.2890, 78.9850], "status": "Watch List", "icon": "plus-sign", "color": "orange", "desc": "Emergency response hub; structural tilts stable but inside perimeter zone."}
]

# --- 3. Sidebar GIS Controls ---
st.sidebar.header("🗺️ GIS Overlay Controls")

map_type = st.sidebar.selectbox(
    "Google Maps Baseline Layer:",
    ["Terrain", "Satellite", "Hybrid", "Roadmap"]
)

show_heatmap = st.sidebar.checkbox("Render Zone Risk Heatmap", value=True)
show_markers = st.sidebar.checkbox("Show Sensor Nodes", value=False)

st.sidebar.subheader("🏢 Infrastructure Filters")
selected_asset_types = st.sidebar.multiselect(
    "Filter Vulnerable Assets:",
    options=["Road", "Village", "Critical Infrastructure"],
    default=["Road", "Village", "Critical Infrastructure"]
)

# --- 4. Main GIS Visual Mapping View ---
col1, col2 = st.columns([2, 1]) # Structured width scaling ratio

with col1:
    st.subheader("🌐 Dynamic Spatial Risk Map")
    
    map_center = [30.3500, 79.2000] 
    sih_map = folium.Map(location=map_center, zoom_start=8, tiles=None)

    google_tiles = {
        "Roadmap": 'https://google.com{x}&y={y}&z={z}',
        "Satellite": 'https://google.com{x}&y={y}&z={z}',
        "Terrain": 'https://google.com{x}&y={y}&z={z}',
        "Hybrid": 'https://google.com{x}&y={y}&z={z}'
    }
    
    folium.TileLayer(
        tiles=google_tiles[map_type],
        attr=f'Google {map_type}',
        name=f'Google Maps ({map_type})',
        overlay=False,
        control=False
    ).add_to(sih_map)

    # LAYER A: Density Heatmap Matrix
    if show_heatmap:
        heat_data = [[spot["coords"][0], spot["coords"][1], spot["intensity"]] for spot in landslide_sensors]
        HeatMap(
            heat_data,
            radius=35,
            blur=20,
            min_opacity=0.4,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1.0: 'red'}
        ).add_to(sih_map)

    # LAYER B: Sensor Station Points
    if show_markers:
        for spot in landslide_sensors:
            folium.CircleMarker(
                location=spot['coords'],
                radius=8,
                color=spot['color'],
                fill=True,
                popup=f"Telemetry Node: {spot['name']}<br>Risk Factor: {spot['risk']}"
            ).add_to(sih_map)

    # LAYER C: Infrastructure Priority Layer
    for asset in infrastructure_assets:
        if asset["type"] in selected_asset_types:
            popup_content = f"""
            <div style='font-family: Arial, sans-serif; width: 220px;'>
                <h5 style='margin:0 0 5px 0; color: #333;'><b>{asset['name']}</b></h5>
                <span style='background-color:{asset['color']}; color:white; padding:2px 6px; border-radius:3px; font-size:10px;'>
                    {asset['status']}
                </span>
                <p style='margin: 8px 0 0 0; font-size:12px;'><b>Category:</b> {asset['type']}</p>
                <p style='margin: 3px 0 0 0; font-size:11px; color:#555;'>{asset['desc']}</p>
            </div>
            """
            folium.Marker(
                location=asset['coords'],
                popup=folium.Popup(popup_content, max_width=260),
                icon=folium.Icon(color=asset['color'] if asset['color'] != 'darkred' else 'red', icon=asset['icon'], prefix='glyphicon')
            ).add_to(sih_map)

    # Render Map Securely
    st_folium(sih_map, width="100%", height=600, key="sih_gis_map")

# --- 5. Downstream Infrastructure Analytics Panel ---
with col2:
    st.subheader("🚨 Risk Mitigation Matrix")
    st.markdown("Algorithmic priority routing based on immediate hazard index intersections.")

    df_assets = pd.DataFrame(infrastructure_assets)
    df_filtered = df_assets[df_assets["type"].isin(selected_asset_types)].copy() # Added .copy() to stop setting-with-copy issues
    
    if not df_filtered.empty:
        priority_order = {"Critical Priority": 0, "High Priority": 1, "Watch List": 2, "Safe / Stable": 3}
        df_filtered["priority_score"] = df_filtered["status"].map(priority_order)
        df_filtered = df_filtered.sort_values(by="priority_score").drop(columns=["priority_score"])

        for _, row in df_filtered.iterrows():
            if "Critical" in row['status'] or "High" in row['status']:
                st.error(f"**[🚨 {row['status'].upper()}] {row['name']}** ({row['type']})")
                st.caption(row['desc'])
            elif "Watch" in row['status']:
                st.warning(f"**[⚠️ {row['status'].upper()}] {row['name']}** ({row['type']})")
                st.caption(row['desc'])
            else:
                st.success(f"**[✅ {row['status'].upper()}] {row['name']}** ({row['type']})")
                st.caption(row['desc'])
            st.divider()
    else:
        st.info("No infrastructure nodes selected.")
