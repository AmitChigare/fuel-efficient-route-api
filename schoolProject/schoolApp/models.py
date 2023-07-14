from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=6)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Add other fields as needed

    def __str__(self):
        return self.name
