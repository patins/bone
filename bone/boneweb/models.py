from django.db import models
from django.contrib.auth.models import User

def _picture_upload_to(resident, filename):
    return 'residents/{0}.{1}'.format(resident.kerberos, filename.split('.')[-1])

class Resident(models.Model):
    name = models.CharField(max_length=200)
    kerberos = models.CharField(max_length=50, unique=True, db_index=True)
    bio = models.TextField(blank=True)
    nickname = models.CharField(max_length=200, blank=True)
    year = models.PositiveSmallIntegerField()
    picture = models.ImageField(upload_to=_picture_upload_to, blank=True)
    visible = models.BooleanField(default=False)
    user = models.OneToOneField(User, null=True, blank=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.kerberos)
