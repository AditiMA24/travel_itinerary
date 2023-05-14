####CREATE map html
# Create a map centered on India
india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Create a dictionary to store colors for each day
color_map = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'purple',
    5: 'yellow',
    6: 'pink',
    7: 'orange',
    8: 'cyan',
    9: 'magenta',
    10: 'brown',
    11: 'gray',
    12: 'olive',
    13: 'lime',
    14: 'teal',
    15: 'navy'
}

def extract_coordinates(lat_lon_str):
    coordinates = re.findall(r'\d+\.\d+', lat_lon_str)
    return [float(coord) for coord in coordinates]

destination_data = df[df['within_time_limit'] == True].groupby('day')[['destination', 'Latitude', 'Longitude']].apply(lambda x: [[row[0], *extract_coordinates(row[1]), *extract_coordinates(row[2])] for _, row in x.iterrows()]).to_dict()

# Create a marker cluster group
marker_cluster = MarkerCluster().add_to(india_map)

# Iterate over the destination_data dictionary
for day, destinations in destination_data.items():
    # Get the color for the current day
    color = color_map.get(day, 'gray')

    # Create a feature group for markers and polyline of the current day
    day_group = folium.FeatureGroup(name=f"Day {day}")

    # Iterate over destinations of the current day
    for i, (destination, lat, lon) in enumerate(destinations, start=1):
        # Add a marker with the corresponding color and number
        folium.Marker(
            location=[lat, lon],
            popup=destination,
            icon=folium.Icon(color=color),
            tooltip=str(i)  # Set the tooltip as the marker number
        ).add_to(marker_cluster)  # Add the marker to the marker cluster

    # Create a polyline for the current day
    locations = [(lat, lon) for _, lat, lon in destinations]
    folium.PolyLine(locations, color=color, weight=3, opacity=0.8, smooth_factor=1).add_to(day_group)

    # Add the feature group to the map
    day_group.add_to(india_map)

# Adjust the zoom to fit the markers and polylines
india_map.fit_bounds(india_map.get_bounds())

# Add a layer control to the map
folium.LayerControl().add_to(india_map)

# Save the map as an HTML file
india_map.save('my_map.html')

# Display the map in Colab
display(india_map)