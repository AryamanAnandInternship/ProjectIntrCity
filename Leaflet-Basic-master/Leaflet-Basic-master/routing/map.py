import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim


df = pd.read_csv('bus_service_run_eta_details.csv')

def get_coordinates(point_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(point_name)
    return (location.latitude, location.longitude)

df['lat'], df['lon'] = zip(*df['point_name'].apply(get_coordinates))

# Calculate the center of the map
map_center = [df['lat'].mean(), df['lon'].mean()]

# Create the map
map = folium.Map(location=map_center, zoom_start=8)

# Create a route PolyLine
route = df[['lat', 'lon']].values.tolist()
folium.PolyLine(route, color="red", weight=2, opacity=1).add_to(map)

# Add text to the PolyLine
folium.PolyLineTextPath(route, 'Schedule', repeat=True, center=True, fill_color='blue', size=8).add_to(map)

# Create MarkerCluster for point markers
point_markers = MarkerCluster().add_to(map)

# Add markers for each point
for index, row in df.iterrows():
    color = 'green' if row['feed_time'] <= row['sch_time'] else 'red'
    popup_text = f"{row['point_name']} - Delay: {row['feed_time'] > row['sch_time']}"
    folium.Marker([row['lat'], row['lon']], popup=popup_text, icon=folium.Icon(color=color)).add_to(point_markers)

# Save the map
map.save('index.html')
