import pandas as pd
import pandas as pd
import folium
from geopy.geocoders import Nominatim

def cleanData(filepath, writepath):
    df = pd.read_csv(filepath) # Load CSV
    df = df.drop([0, 1]) # Drop rows 2 and 3 (qualtrics import vars)
    df = df[df['Finished'] == "True"] # Filter rows where 'Finished' is TRUE
    df = df.rename(columns={'Status.1': "status"})
    df = df[['ResponseId','status','latitude', 'longitude']] # Keep relevant cols
    df = df.dropna() #Remove missing values (note forced responses now in Qualtrics)
    # Convert 'latitude' and 'longitude' to floats
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df.to_csv(writepath)
    return(df)
    

def createDepartmentOriginsMap(df):
    # df = pd.read_excel(df)
    # Colours
    colours = {'Undergraduate': '#2D7DD2',
               'Postgraduate Taught': '#97CC04',
               'PhD': '#EEB902',
               'Staff': '#F45D01'
               }


    # Create a folium map centered on University of Sussex, Brighton, UK
    geolocator = Nominatim(user_agent="institution_mapper")
    sussex_coords = geolocator.geocode("University of Sussex, Brighton, UK")
    map_center = [sussex_coords.latitude/2, sussex_coords.longitude+15]
    map = folium.Map(location=map_center, zoom_start=3)

    # Add polylines first
    for _, row in df.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            status = row['status']
            
            # Add line from the institution to University of Sussex
            folium.PolyLine(
                locations=[[row['latitude'], row['longitude']], [sussex_coords.latitude, sussex_coords.longitude]],
                tooltip=status,
                color='lightgrey',
                weight=1,
                opacity=1
                # dash_array='10'
            ).add_to(map)

    # Add markers on top
    for _, row in df.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            status = row['status']
            
            # Create circle marker with size proportional to 'Outputs'
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,  # Adjust scaling factor as needed
                popup=f"<strong>{status}</strong>",
                color=colours[status], #'#013d4b',
                fill=True,
                fill_opacity=0.7
            ).add_to(map)

    # Finally, add a marker for University of Sussex
    icon = folium.CustomIcon("Co-authorship/US_border.png", icon_size=(50, 50))

    folium.Marker(
        location=[sussex_coords.latitude, sussex_coords.longitude],
        popup="University of Sussex",
        icon=icon
    ).add_to(map)

    # Save the map to an HTML file
    map.save('docs/origins/index.html')

if __name__ == "__main__":
    df = cleanData('Department Origins/Data/Student origin map_28 October 2024_10.47.csv', 'Department Origins/Data/origins_clean.csv')
    createDepartmentOriginsMap(df)
