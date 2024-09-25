# Required libraries
import folium
from geopy.geocoders import Nominatim

# List of university names
universities = [
    "Harvard University, USA",
    "University of Oxford, UK",
    "Stanford University, USA",
    "Massachusetts Institute of Technology, USA",
    "University of Cambridge, UK",
    "California Institute of Technology, USA",
    "University of Chicago, USA",
    "Princeton University, USA",
    "Columbia University, USA",
    "University of Toronto, Canada"
]

# Initialize the geocoder
geolocator = Nominatim(user_agent="university_mapper")

# Function to get coordinates for a list of places
def get_coordinates(places):
    coordinates = []
    for place in places:
        location = geolocator.geocode(place)
        if location:
            coordinates.append((location.latitude, location.longitude, place))
    return coordinates

# Get coordinates for the universities
university_coordinates = get_coordinates(universities)

# Create a base map centered around the mean latitude and longitude
mean_lat = sum([lat for lat, lon, name in university_coordinates]) / len(university_coordinates)
mean_lon = sum([lon for lat, lon, name in university_coordinates]) / len(university_coordinates)
map_universities = folium.Map(location=[mean_lat, mean_lon], zoom_start=2)

# Add university markers to the map
for lat, lon, name in university_coordinates:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(map_universities)

# Save map to HTML file
map_path = "/mnt/data/university_map.html"
map_universities.save(map_path)

map_path