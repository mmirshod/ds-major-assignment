import heapq
import os
from math import radians, cos, sin, atan2, sqrt, ceil

import folium
import osmnx as ox


def a_star_search(graph, start, goal):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        (cost, node, path) = heapq.heappop(pq)

        if node not in visited:
            visited.add(node)
            path = path + [node]

            if node == goal:
                return path

            for neighbor, data in graph[node].items():
                if neighbor not in visited:
                    edge_length = data.get('length', 1)  # Assuming 'length' is the key for edge length
                    heapq.heappush(pq, (cost + edge_length, neighbor, path))

    return None


def haversine_distance(lat1, lon1, lat2, lon2) -> int:
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return int(distance)


def calculate_midpoint(lat1, lon1, lat2, lon2):
    # Calculate the midpoint between two locations
    midpoint_lat = (lat1 + lat2) / 2
    midpoint_lon = (lon1 + lon2) / 2

    return midpoint_lat, midpoint_lon


def generate_shortest_path(origin, destination):

    # Convert place names to locations
    origin_loc = ox.geocode(origin)
    destination_loc = ox.geocode(destination)

    # Find haversine distance and middle point

    # multiply by 1000 to get distance in meters
    dist = ceil(haversine_distance(origin_loc[0], origin_loc[1], destination_loc[0], destination_loc[1]) * 1000)
    mid_point = calculate_midpoint(origin_loc[0], origin_loc[1], destination_loc[0], destination_loc[1])

    # Generate road network graph
    print("Gathering fresh datasets...")
    G = ox.graph_from_point(mid_point, network_type="drive", dist=(dist + 500))

    # Convert locations to nodes
    origin_node = ox.nearest_nodes(G, origin_loc[1], origin_loc[0])
    destination_node = ox.nearest_nodes(G, destination_loc[1], destination_loc[0])

    print("Searching for shortest route...")
    shortest_path_nodes = a_star_search(G, start=origin_node, goal=destination_node)
    shortest_path_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path_nodes]

    return shortest_path_coordinates


def visualize_map(origin, dest):

    # Check whether user has already searched this path
    filename = f"paths/path_from_{origin.replace(' ', '_')}_to_{dest.replace(' ', '_')}.html"

    # If true, then show to user previous response.
    if os.path.exists(filename):
        print("You have searched this path before. Showing previous response...")
        os.system(f"start {filename}")
        return

    # Generate the shortest path
    path = generate_shortest_path(origin=origin, destination=dest)

    # Create Map object with initial location
    map_obj = folium.Map(location=path[0], zoom_start=14)

    # Marker origin and destination points
    folium.Marker(location=path[0], popup="Origin").add_to(map_obj)
    folium.Marker(location=path[-1], popup="Destination").add_to(map_obj)

    # Plot path
    folium.PolyLine(locations=path, color="blue", weight=2.5, opacity=1).add_to(map_obj)

    if not os.path.exists("paths"):
        os.makedirs("paths")

    map_obj.save(filename)
    os.system(f"start {filename}")


if __name__ == "__main__":
    # Get user input
    origin_place = input("Enter name of origin place: ")
    destination_place = input("Enter name of destination place: ")

    # Run the program
    visualize_map(origin=origin_place, dest=destination_place)
