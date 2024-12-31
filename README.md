
# Trip Planner Using Dijkstra's Algorithm 🚗🗺️

Welcome to the **Trip Planner**! This Python-based application helps you plan your trips by calculating the shortest path using **Dijkstra's Algorithm**. With a simple interface, it calculates routes, distances, and travel times using external APIs. 🛣️

## Features 🔑
- **Route Calculation** 🛤️: Calculates the shortest route between two points using **Dijkstra's Algorithm**.
- **Multiple Travel Modes** 🚗: Choose from different travel modes (Car, Bike, Bus).
- **Distance and Time Estimates** ⏱️: Get accurate travel time and distance estimates.
- **User-Friendly Interface** 👩‍💻: Intuitive interface built using **Tkinter**.
- **API Integration** 🌐: Uses **OpenRouteService** and **Nominatim** APIs to fetch travel data.
- **Error Handling** 🚫: Handles incorrect inputs and missing data.

## How It Works ⚙️
1. **Set Start and End Locations** 📍: Enter your starting and ending locations.
2. **Select Travel Mode** 🚗: Choose between Car, Bike, or Bus for customized estimates.
3. **View Results** 🏁: Get the shortest route, distance, and estimated time of travel.
4. **Interactive Map** 🗺️: Visualize your journey with route information displayed.

## Installation 🛠️
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/Trip-Planner-Using-Dijkstra.git
```

Then, run the application:

```bash
python trip_planner.py
```

## Requirements 📦
- Python 3.x
- **Tkinter** (comes with Python by default)
- **Requests**: For API calls. Install it using `pip install requests`.
- **OpenRouteService** API key (sign up at [OpenRouteService](https://openrouteservice.org/) for an API key).
- **Nominatim** API (free for low traffic use, part of **OpenStreetMap**).

## License 📝
This project is licensed under the MIT License.
