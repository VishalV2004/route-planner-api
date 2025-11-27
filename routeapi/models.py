from django.db import models

class FuelStation(models.Model):
    station_id = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    rack_id = models.IntegerField(null=True, blank=True)
    price_per_gallon = models.FloatField()
    latitude = models.FloatField(default=0.0)       # Placeholder (optional)
    longitude = models.FloatField(default=0.0)      # Placeholder (optional)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"
