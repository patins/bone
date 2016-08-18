from django.db import models
from boneweb.models import Resident

class Tinder(models.Model):
    resident = models.OneToOneField(Resident)
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True)

    def __str__(self):
        return "Tinder <{}>".format(self.resident)

    class Meta:
        permissions = (
            ("view_all", "Can view all Tinders and bulk output"),
        )

    def completed(self):
        return not (self.bio == "" or self.age == "" or self.name == "" or self.picture == "" or self.location == "")
