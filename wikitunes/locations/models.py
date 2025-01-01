from django.db import models

from content.models import acc_data_desc_dir_path
from django.contrib.gis.db import models as gis_models

class Location(gis_models.Model):
    """
    Represents a geolocation associated to an account, event or forum.
    """
    name = models.CharField(max_length=255, help_text="name of location")
    description = models.FileField(upload_to=acc_data_desc_dir_path, help_text="Location describing the post content.")
    added_by = models.CharField(max_length=255, help_text="name of locator")
    address = models.CharField(max_length=255, help_text="Full address of the location.")
    latitude = models.FloatField(help_text="Latitude of the location.")
    longitude = models.FloatField(help_text="Longitude of the location.")
    coordinates = gis_models.PointField(geography=True, help_text="Geographic coordinates (latitude, longitude).")

    def __str__(self):
        return self.address
