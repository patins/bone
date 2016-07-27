from django.test import TestCase
from django.test import Client

from boneweb.models import Resident
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='insinger')
        self.resident = Resident.objects.create(
            name='Patrick',
            kerberos='insinger',
            year=2019,
            user=user
        )
        self.c = Client()
        self.c.force_login(user)
    def test_profile(self):
        r = self.c.get('/profile/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b"insinger's Profile", r.content)
    def test_update_info(self):
        r = self.c.post('/profile/', {'bio': "mynewbio", 'name': "newname"})
        self.assertEqual(200, r.status_code)
        self.assertIn(b"mynewbio", r.content)
        self.assertIn(b"newname", r.content)
        self.resident.refresh_from_db()
        self.assertEqual(self.resident.bio, "mynewbio")
        self.assertEqual(self.resident.name, "newname")
    def tearDown(self):
        Resident.objects.all().delete()
        User.objects.all().delete()
