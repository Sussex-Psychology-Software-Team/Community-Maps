import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

def createMap(data_path, out_path):
    # Create a folium map centered on University of Sussex, Brighton, UK
    geolocator = Nominatim(user_agent="institution_mapper")
    sussex_coords = geolocator.geocode("University of Sussex, Brighton, UK")
    map_center = [sussex_coords.latitude/2, sussex_coords.longitude+15]
    map_institutions = folium.Map(location=map_center, zoom_start=3)

    # Add markers for other universities
    try:
        df = pd.read_csv(data_path, encoding='utf-8')
    except:
        df = pd.read_excel(data_path, encoding='utf-8')

    # Add polylines first
    for _, row in df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            institution = row['Institutions']
            # outputs = row['Outputs']
            
            # Add line from the institution to University of Sussex
            folium.PolyLine(
                locations=[[row['Latitude'], row['Longitude']], [sussex_coords.latitude, sussex_coords.longitude]],
                tooltip=institution,
                color='lightgrey',
                weight=1,
                opacity=0.5
                # dash_array='10'
            ).add_to(map_institutions)

    # Add markers on top
    for _, row in df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            institution = row['Institutions']
            # outputs = row['Outputs']
            
            # Create circle marker with size proportional to 'Outputs'
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=1,#outputs/4,  # Adjust scaling factor as needed
                popup=f"<strong>{institution}</strong>",
                color='#013d4b',
                fill=True,
                fill_opacity=0.7
            ).add_to(map_institutions)

    # Finally, add a marker for University of Sussex
    icon = folium.CustomIcon("CRCSD/US_border.png", icon_size=(50, 50))

    folium.Marker(
        location=[sussex_coords.latitude, sussex_coords.longitude],
        popup="University of Sussex",
        icon=icon
    ).add_to(map_institutions)

    # Save the map to an HTML file
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    map_institutions.save(out_path)

