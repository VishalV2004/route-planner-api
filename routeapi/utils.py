import openrouteservice
from django.conf import settings
from haversine import haversine
from .models import FuelStation

client = openrouteservice.Client(key=settings.ORS_API_KEY)


# -----------------------------
# GEOCODING
# -----------------------------
def geocode_address(address):
    res = client.pelias_search(text=address)
    if not res or "features" not in res or len(res["features"]) == 0:
        raise ValueError(f"Geocoding failed for address: {address}")

    coords = res["features"][0]["geometry"]["coordinates"]  # lon, lat
    return (coords[1], coords[0])  # lat, lon


# -----------------------------
# ROUTE
# -----------------------------
def get_route(start_coords, end_coords):
    coords = [(start_coords[1], start_coords[0]), (end_coords[1], end_coords[0])]

    route = client.directions(coords, profile="driving-car", format="geojson")

    geometry = route["features"][0]["geometry"]["coordinates"]
    segment = route["features"][0]["properties"]["segments"][0]

    route_points = [(latlng[1], latlng[0]) for latlng in geometry]

    return {
        "route_points": route_points,
        "distance_m": segment["distance"],
        "duration_s": segment["duration"]
    }


# -----------------------------
# STATION DISTANCE TO ROUTE
# -----------------------------
def nearest_distance_to_route(station, route_points):
    return min(haversine((station.latitude, station.longitude), p) for p in route_points)


# -----------------------------
# SMARTEST FUEL STOP LOGIC
# -----------------------------
def find_cheapest_stops(route_points, vehicle_range=500):
    stations = FuelStation.objects.all()

    # stations within 50 miles of the route corridor
    corridor_stations = []
    for s in stations:
        d = nearest_distance_to_route(s, route_points)
        if d <= 50:
            corridor_stations.append((s, d))

    # Sort by cheapest price
    corridor_stations = sorted(corridor_stations, key=lambda x: x[0].price_per_gallon)

    # Deduplicate by name + city
    unique = {}
    for s, d in corridor_stations:
        key = (s.name.strip().lower(), s.city.strip().lower())
        if key not in unique:
            unique[key] = (s, d)

    # return top 3
    final_stations = []
    for s, d in list(unique.values())[:3]:
        final_stations.append({
            "name": s.name,
            "city": s.city,
            "state": s.state,
            "price": s.price_per_gallon,
            "lat": s.latitude,
            "lng": s.longitude,
            "distance_from_route_miles": round(d, 2)
        })

    return final_stations
