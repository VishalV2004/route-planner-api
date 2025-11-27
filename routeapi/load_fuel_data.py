import pandas as pd
import os
import django
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from routeapi.models import FuelStation

# Path to CSV
csv_file_path = os.path.join(project_root, "fuel_prices.csv")

print(f"Loading data from: {csv_file_path}")

try:
    # Load CSV
    df = pd.read_csv(csv_file_path)

    # Show CSV columns
    print(f"CSV Columns found: {list(df.columns)}")

    # EXPECTED COLUMNS:
    # station_id, name, address, city, state, rack_id, price

    count = 0
    for _, row in df.iterrows():

        FuelStation.objects.update_or_create(
            station_id=row['station_id'],
            defaults={
                "name": row['name'],
                "address": row['address'],
                "city": row['city'],
                "state": row['state'],
                "rack_id": row['rack_id'],
                "price_per_gallon": row['price'],
                "latitude": 0.0,   # placeholder
                "longitude": 0.0   # placeholder
            }
        )
        count += 1

    print(f"Successfully loaded {count} fuel stations into the database!")

except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    print("Make sure 'fuel_prices.csv' is in your project root folder.")

except KeyError as e:
    print(f"Error: Column not found in CSV: {e}")
    print("Your script expects the following CSV columns:")
    print("['station_id', 'name', 'address', 'city', 'state', 'rack_id', 'price']")
    print(f"Columns in your CSV: {list(df.columns)}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
