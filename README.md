🚀 Route Planner API with Optimal Fuel Stops

A Django REST API that calculates the driving route between two U.S. locations and finds the cheapest fuel stations along the route.
It uses OpenRouteService (ORS) for routing + geocoding and analyzes thousands of fuel stations to recommend optimal stops.

Includes:

Full route polyline

Distance & travel time

Fuel consumption

Cost estimation

3 cheapest fuel stations near your route

Frontend map viewer (Leaflet)

🗺️ Live Demo (Local)

When running locally:

http://127.0.0.1:8000/api/route/?start=Dallas,TX&end=Houston,TX


Map Viewer UI:

http://127.0.0.1:8000/map/

📌 Features
✅ Route Calculation

Uses OpenRouteService API

Full polyline returned for map rendering

✅ Fuel Stop Optimization

Finds stations:

Within 50 miles of route

Removes duplicates

Ranks by cheapest fuel price

✅ Fuel Cost Estimate

Assumes:

10 miles per gallon

Total cost = gallons × average stop price

✅ Extra Metadata Returned

Distance in miles

Travel time

Fuel needed

Cost estimate

Route geometry

Fuel stop details (lat/lng, distance from route)

🛠️ Tech Stack
Backend

Python (Django REST Framework)

OpenRouteService (ORS)

Haversine distance calculation

SQLite database

Frontend

HTML + CSS

Leaflet.js map visualization

📂 Project Structure
route-planner-api/
│
├── core/
│   ├── settings.py
│   ├── urls.py
│
├── routeapi/
│   ├── models.py
│   ├── views.py
│   ├── utils.py
│   ├── load_fuel_data.py
│   ├── urls.py
│
├── templates/
│   └── map.html
│
├── fuel_prices.csv
├── manage.py
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/VishalV2004/route-planner-api.git
cd route-planner-api

2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your ORS API Key

Open:

core/settings.py


Add:

ORS_API_KEY = "YOUR_KEY_HERE"

5️⃣ Run migrations
python manage.py migrate

6️⃣ Load fuel data
python routeapi/load_fuel_data.py

7️⃣ Start server
python manage.py runserver

🔗 API Usage
Endpoint:
GET /api/route/?start=<city1>&end=<city2>

Example:
/api/route/?start=Dallas,TX&end=Houston,TX

Sample JSON Response:
{
  "start": "Dallas,TX",
  "end": "Houston,TX",
  "distance_miles": 235.32,
  "travel_time_minutes": 224.5,
  "fuel_needed_gallons": 23.53,
  "estimated_cost": 68.71,
  "fuel_stops": [
    {
      "name": "Pilot Travel Center",
      "city": "Corsicana",
      "state": "TX",
      "price": 2.85,
      "lat": 32.0954,
      "lng": -96.4689,
      "distance_from_route_miles": 2.62
    }
  ],
  "route_polyline": [...]
}

🌍 Frontend Map Viewer

Visit:

http://127.0.0.1:8000/map/


Shows:

Route polyline

Fuel station markers

Prices + distance in popup

🧪 Testing in Django Shell
python manage.py shell


Then:

from routeapi.utils import geocode_address, get_route, find_cheapest_stops

👨‍💻 Author

Vishal V
GitHub: https://github.com/VishalV2004

🎯 Notes

ORS free tier supports 2,500 requests/day.

Good enough for assignments & demos.

Deployment optional — GitHub project alone is acceptable for submission.
