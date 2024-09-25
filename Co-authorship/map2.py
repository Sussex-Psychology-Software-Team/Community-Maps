import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Create a folium map centered on University of Sussex, Brighton, UK
geolocator = Nominatim(user_agent="institution_mapper")
sussex_coords = geolocator.geocode("University of Sussex, Brighton, UK")
map_center = [sussex_coords.latitude, sussex_coords.longitude]
map_institutions = folium.Map(zoom_start=2) #location=map_center, 

# Add markers for other universities
file_path = 'Co-authorship/geolocated_data.csv'  # Replace with the actual file path
df = pd.read_csv(file_path)

# Add polylines first
for _, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        institution = row['Institutions']
        outputs = row['Outputs']
        
        # Add line from the institution to University of Sussex
        folium.PolyLine(
            locations=[[row['Latitude'], row['Longitude']], [sussex_coords.latitude, sussex_coords.longitude]],
            tooltip=institution,
            color='grey',
            weight=1,
            opacity=0.2,
            dash_array='10'
        ).add_to(map_institutions)

# Add markers on top
for _, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        institution = row['Institutions']
        outputs = row['Outputs']
        
        # Create circle marker with size proportional to 'Outputs'
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=outputs/2,  # Adjust scaling factor as needed
            popup=f"<strong>{institution}</strong><br><br><i>{outputs} outputs</i>",
            color='blue',
            fill=True,
            fill_opacity=0.7
        ).add_to(map_institutions)

# Finally, add a marker for University of Sussex
icon = folium.CustomIcon("Co-authorship/US.png", icon_size=(50, 50))

folium.Marker(
    location=[sussex_coords.latitude, sussex_coords.longitude],
    popup="University of Sussex",
    icon=icon
).add_to(map_institutions)

# Save the map to an HTML file
map_institutions.save('Co-authorship/institutions_map.html')

