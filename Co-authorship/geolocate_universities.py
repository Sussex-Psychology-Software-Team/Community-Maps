import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3

# Load the dataset
file_path = 'Co-authorship/international data from darya.xlsx'
df = pd.read_excel(file_path)

# Initialize geocoder
geolocator = Nominatim(user_agent="institution_mapper")
# Initialize Google Geocoder (requires an API key)
api_key='AIzaSyDIQRxP8rBb-MRF-qJ2kwoNEUSMIuGKFHw'
if(api_key != ''):
    google_geolocator = GoogleV3(api_key=api_key)

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Manual geocodes dictionary for known universities
manual_geocodes = {
    "Some University Name": (51.509865, -0.118092),
    "Another University": (40.712776, -74.005974),
}

# Function to get coordinates, skipping geocoding if lat/long already exists
# Function to get coordinates, skipping geocoding if lat/long already exists
def get_coordinates(row):
    # Check if there are already valid coordinates
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        print('Datapoint already found')
        return row['Latitude'], row['Longitude']
    
    # Check for manual geocodes
    place = row['Institutions']
    if place in manual_geocodes:
        print("Datapoint in manual specified")
        return manual_geocodes[place]
    else: 
        # Geocode the institution using Nominatim or fallback to Google
        try:
            location = geolocator.geocode(place)
            if location:
                return location.latitude, location.longitude
            else:
                print(f"Nominatim couldn't find {place}")
                # If Google API key is provided, fallback to Google geocoding
                if api_key != '':  # Check if the API key is present
                    print(f"Trying Google Geocoding for {place}")
                    location = google_geolocator.geocode(place)
                    if location:
                        print("Found with Google")
                        return location.latitude, location.longitude
                    else:
                        print('Google couldn\'t find it either')
                else:
                    print("Google Geocoding skipped due to missing API key")
                return None, None
        except Exception as e:
            print(f"Error geocoding {place}: {e}")
            return None, None

# Add latitude and longitude columns if they don't exist
if 'Latitude' not in df.columns:
    df['Latitude'] = None
if 'Longitude' not in df.columns:
    df['Longitude'] = None

# Apply the function to each row of the DataFrame
df['Latitude'], df['Longitude'] = zip(*df.apply(get_coordinates, axis=1))

# Output the resulting DataFrame and save to CSV
print(df)
df.to_excel(file_path, index=False)
df.to_csv('Co-authorship/geolocated_data.csv', index=False)
