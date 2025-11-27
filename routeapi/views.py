from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .utils import geocode_address, get_route, find_cheapest_stops


class RouteAPIView(APIView):
    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")

        if not start or not end:
            return Response({"error": "start and end parameters are required"}, status=400)

        try:
            start_coords = geocode_address(start)
            end_coords = geocode_address(end)

            route = get_route(start_coords, end_coords)
            distance_miles = round(route["distance_m"] / 1609.34, 2)
            time_minutes = round(route["duration_s"] / 60, 2)

            fuel_needed = round(distance_miles / 10, 2)

            stops = find_cheapest_stops(route["route_points"])
            avg_price = sum(s["price"] for s in stops) / len(stops) if stops else 0

            total_cost = round(fuel_needed * avg_price, 2)

            return Response({
                "start": start,
                "end": end,
                "distance_miles": distance_miles,
                "travel_time_minutes": time_minutes,
                "fuel_needed_gallons": fuel_needed,
                "estimated_cost": total_cost,
                "fuel_stops": stops,
                "route_polyline": route["route_points"]
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
class MapView(TemplateView):
    template_name = "map.html"

