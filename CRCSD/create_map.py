from geocoder import geolocate
from map import createMap

API_KEY = "AIzaSyCAIQUuKwQOAAxNZQvXqLLtuDN75lfyeIA"
df = geolocate('CRCSD/CRCSD_Institutions.csv', 'CRCSD/CRCSD_Institutions.csv', API_KEY)
createMap('CRCSD/CRCSD_Institutions.csv', 'docs/CRCSD/index.html')