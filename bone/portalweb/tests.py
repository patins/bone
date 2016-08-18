from django.test import TestCase
from django.test import Client

from boneweb.models import Resident
from django.contrib.auth.models import User

from urllib.parse import urlparse, parse_qs

class AuthenticationTestCase(TestCase):
    def setUp(self):
        Resident.objects.create(name='Patrick', kerberos='insinger', year=2019)
    def test_scripts_redirect(self):
        with self.settings(SHIB_RESPONDER_URL='https://bone.mit.edu/Shibboleth.sso'):
            r = Client().get('/login/')
            self.assertEqual(r.status_code, 302)
            self.assertEqual(r.url.split('?')[0], "https://bone.mit.edu/Shibboleth.sso/Login")
            query = parse_qs(urlparse(r.url).query)
            self.assertEqual(query['target'][0], "http://testserver/login/")
    def test_invalid_email(self):
        self.assertLoginFails('insinger@harvard.edu')
    def test_no_resident(self):
        self.assertLoginFails('aveni@mit.edu')
    def test_valid(self):
        c = Client()
        r = Client().get('/login/', HTTP_EPPN='insinger@MIT.edu')
        self.assertRedirects(r, '/profile/')
        self.assertTrue(User.objects.filter(username='insinger').exists())
    def tearDown(self):
        Resident.objects.all().delete()
        User.objects.all().delete()
    def assertLoginFails(self, eppn):
        r = Client().get('/login/', HTTP_EPPN=eppn)
        self.assertIn(b'Failure', r.content)

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

class TinderTestCase(TestCase):
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
    def test_make_tinder_notification(self):
        r = self.c.get('/profile/')
        self.assertIn(b"Start your Tinder profile!", r.content)
        r = self.c.get('/tinder/')
        self.assertEqual(200, r.status_code)
        r = self.c.get('/profile/')
        self.assertIn(b"Your Tinder is not yet completed!", r.content)
    def test_tinder_preview(self):
        r = self.c.get('/tinder/')
        self.assertIn(b"Your Tinder", r.content)
    def test_update_tinder_info(self):
        r = self.c.post('/tinder/', {'name': "newname", 'age': "newage", 'bio': "newbio", 'location': "newlocation"})
        self.assertEqual(200, r.status_code)
        self.assertIn(b"newname", r.content)
        self.assertIn(b"newage", r.content)
        self.assertIn(b"newbio", r.content)
        self.assertIn(b"newlocation", r.content)
        self.resident.refresh_from_db()
        self.assertEqual(self.resident.tinder.name, "newname")
        self.assertEqual(self.resident.tinder.age, "newage")
        self.assertEqual(self.resident.tinder.bio, "newbio")
        self.assertEqual(self.resident.tinder.location, "newlocation")
    def tearDown(self):
        Resident.objects.all().delete()
        User.objects.all().delete()
