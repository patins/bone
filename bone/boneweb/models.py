from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from uuid import uuid4

def _picture_upload_to(resident, filename):
    return "residents/{}.{}".format(uuid4().hex, filename.split('.')[-1])

class Resident(models.Model):
    name = models.CharField(max_length=200)
    kerberos = models.CharField(max_length=50, unique=True, db_index=True)
    bio = models.TextField(blank=True)
    nickname = models.CharField(max_length=200, blank=True)
    year = models.PositiveSmallIntegerField()
    picture = ImageField(upload_to=_picture_upload_to, blank=True)
    visible = models.BooleanField(default=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.kerberos)
