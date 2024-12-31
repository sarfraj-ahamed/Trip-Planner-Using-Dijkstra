import requests
import tkinter as tk
from tkinter import messagebox

# Function to create a dropdown menu for transport types
def create_transport_dropdown(root, options, default_option, width):
    # Define a variable to hold the selected option
    selected_option = tk.StringVar(root)
    selected_option.set(default_option)  # Set default option

    # Create and configure the dropdown menu (OptionMenu) with custom width
    dropdown_menu = tk.OptionMenu(root, selected_option, *options)
    dropdown_menu.config(font=("Helvetica", 14), width=width)

    # Pack the dropdown menu into the window
    dropdown_menu.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

    return selected_option  # Return the variable to access the selected option

# Function to get the latitude and longitude of a city using Nominatim API (OpenStreetMap)
def get_coordinates(address):
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
    headers = {
        'User-Agent': 'MyTripPlanner/1.0 (myemail@example.com)'  # Include your contact details
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            print(f"Error: No coordinates found for address: {address}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return None, None

# Function to get the route between two coordinates using OpenRouteService API
def get_route(start_lat, start_lon, end_lat, end_lon, api_key):
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}'
    coordinates = [[start_lon, start_lat], [end_lon, end_lat]]
    payload = {
        "coordinates": coordinates
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'routes' in data and data['routes']:
            distance = data['routes'][0]['summary']['distance'] / 1000  # Convert from meters to kilometers
            duration = data['routes'][0]['summary']['duration'] / 60   # Convert from seconds to minutes
            return distance, duration, data['routes'][0]['segments'][0]['steps']  # Return steps as well
        else:
            print("Error: No route found.")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return None, None, None

# Function to reverse geocode using OpenStreetMap (Nominatim)
def reverse_geocode_osm(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'address' in data:
            city = data['address'].get('city', data['address'].get('town', data['address'].get('village', None)))  # Get the city name from the address
            return city
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during reverse geocode: {e}")
        return None

# Function to get a list of cities along the route using OpenRouteService API
def get_route_cities(start_lat, start_lon, end_lat, end_lon, api_key):
    # Get the route details including distance, duration, and steps
    distance, duration, steps = get_route(start_lat, start_lon, end_lat, end_lon, api_key)
    cities = set()

    # Check if we received valid steps
    if not steps:
        print("Error: No steps found in the route.")
        return []

    # Open the file in write mode to overwrite previous data
    with open("location.txt", "w") as file:
        file.write("Route Steps:\n")
        
        for step in steps:
            # Write the entire step data to the file for debugging
            file.write(f"Step data: {step}\n")

            # Debugging: print the entire step to see what it contains
            print(f"Step data: {step}")

            # Look for location data or geometry data
            location_found = False
            lat, lon = None, None

            # Check if 'location' exists in the step
            if 'location' in step:
                lat, lon = step['location']
                location_found = True
            # If 'geometry' exists, extract coordinates
            elif 'geometry' in step and 'coordinates' in step['geometry']:
                lat, lon = step['geometry']['coordinates'][0], step['geometry']['coordinates'][1]
                location_found = True

            # If location is found, reverse geocode to find the city
            if location_found:
                city = reverse_geocode_osm(lat, lon)
                
                if city:
                    # Add the city to the set to avoid duplicates
                    cities.add(city)
                    file.write(f"City found: {city}\n")  # Write the city name to the file
                else:
                    file.write(f"No city found for coordinates: {lat}, {lon}\n")
            else:
                file.write("No valid location or coordinates found in this step.\n")

        # Write the final cities list
        file.write(f"\nCities covered along the route: {', '.join(cities)}\n")
    
    # Debugging: print the final list of cities covered
    print(f"Cities covered along the route: {cities}")

    # Return the list of cities
    return list(cities)

    # Debugging: print the final list of cities covered
    print(f"Cities covered along the route: {cities}")

    # Return the list of cities
    return list(cities)

    # Debugging: print the final list of cities covered
    print(f"Cities covered along the route: {cities}")

    # Return the list of cities
    return list(cities)


# Function to format the time in days, hours, and minutes
def format_time(duration_minutes):
    duration_minutes = max(duration_minutes, 0)
    days = duration_minutes // (24 * 60)
    hours = (duration_minutes % (24 * 60)) // 60
    minutes = duration_minutes % 60
    return f"{days} days {hours} hours {minutes:.1f} minutes"

# Function to calculate the total cost based on distance
def calculate_cost(distance_km, cost_per_km):
    return distance_km * cost_per_km

# Function to handle the trip planning
def plan_trip():
    source = source_city_entry.get()
    destination = destination_city_entry.get()
    api_key = '5b3ce3597851110001cf62489fee56e73e5a44ae8792325fffa2d818'

    if not source or not destination:
        messagebox.showerror("Input Error", "Please enter both source and destination cities.")
        return

    # Get coordinates for both cities
    start_lat, start_lon = get_coordinates(source)
    end_lat, end_lon = get_coordinates(destination)

    if start_lat is None or end_lat is None:
        messagebox.showerror("Error", "Unable to get coordinates for one or both of the cities.")
        return

    # Get the route (distance and duration) using OpenRouteService
    distance, duration, _ = get_route(start_lat, start_lon, end_lat, end_lon, api_key)

    if distance is None or duration is None:
        messagebox.showerror("Error", "Unable to get the route.")
        return

    # Get the selected transport type
    transport_type = transport_type_var.get()

    # Initialize cost
    cost = 0

    # Adjust time based on transport type
    if transport_type == "Bike":
        adjusted_duration = max(duration - 50, 0)  # Reduce 10-15 minutes for bike
        result_text.set(f"Distance: {distance:.2f} km\n"
                        f"Time: {format_time(adjusted_duration)}\n"
                        f"Cost: ₹{cost:.2f}")  # No cost for Bike
    elif transport_type == "Car":
        adjusted_duration = duration - 25  # Increase 25 minutes for bus
        result_text.set(f"Distance: {distance:.2f} km\n"
                        f"Time: {format_time(adjusted_duration)}\n"
                        f"Cost: ₹{cost:.2f}")  # No cost for Bus
    else:  # For Car, use original time and calculate cost
        adjusted_duration = duration + 30  # Slightly adjusted for car
        cost = calculate_cost(distance, 0.5)  # Default cost per km ₹0.5
        result_text.set(f"Distance: {distance:.2f} km\n"
                        f"Time: {format_time(adjusted_duration)}\n"
                        f"Cost: ₹{cost:.2f}")

# Create the main window
root = tk.Tk()
root.title("Trip Planner")
root.geometry("600x500")  # Set the window size
root.configure(bg="lightblue")

# Create a frame to hold the form widgets
frame = tk.Frame(root, bg="lightblue")
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Create labels and entries for source and destination
tk.Label(frame, text="Enter Source City:", bg="lightblue", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, sticky="w")
source_city_entry = tk.Entry(frame, font=("Helvetica", 14), width=30)
source_city_entry.grid(row=0, column=1, pady=10, padx=10)

tk.Label(frame, text="Enter Destination City:", bg="lightblue", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, sticky="w")
destination_city_entry = tk.Entry(frame, font=("Helvetica", 14), width=30)
destination_city_entry.grid(row=1, column=1, pady=10, padx=10)

# Create dropdown for transport type
options = ["Car", "Bike", "Bus"]
default_transport = "Car"
transport_type_var = create_transport_dropdown(frame, options, default_transport, 30)

# Create a button to trigger the trip planning
plan_button = tk.Button(frame, text="Plan Trip", font=("Helvetica", 14), command=plan_trip)
plan_button.grid(row=3, column=0, columnspan=2, pady=20)

# Create a label to display the results
result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, bg="lightblue", font=("Helvetica", 14), justify="left")
result_label.grid(row=4, column=0, columnspan=2, pady=20)

# Start the Tkinter event loop
root.mainloop()
