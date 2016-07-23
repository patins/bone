from django.test import TestCase
from django.test import Client
from django.conf import settings

from urllib.parse import urlparse, parse_qs, urlencode

from boneweb.models import Resident
from django.contrib.auth.models import User

import hmac
import hashlib

class AuthenticationTestCase(TestCase):
    def setUp(self):
        Resident.objects.create(name='Patrick', kerberos='insinger', year=2019)
    def test_scripts_redirect(self):
        r = Client().get('/login/')
        self.assertEqual(r.status_code, 302)
        query = parse_qs(urlparse(r.url).query)
        self.assertEqual(len(query['token'][0]), 32)

        self.assertEqual(r.url, \
                        "{}?token={}".format(settings.SCRIPTS_AUTH_URL, query['token'][0]))
    def test_invalid_token(self):
        self.assertLoginFails('/login/?{}'.format(urlencode({
            'email': 'insinger@MIT.edu',
            'signature': 'abc123'
        })))
    def test_invalid_token(self):
        client = Client()
        url = self.create_valid_login_url('insinger@harvard.edu', client)
        self.assertLoginFails(url, client)
    def test_no_resident(self):
        client = Client()
        url = self.create_valid_login_url('aveni@mit.edu', client)
        self.assertLoginFails(url, client)
    def test_valid(self):
        c = Client()
        r = c.get(self.create_valid_login_url('insinger@MIT.edu', c))
        self.assertRedirects(r, '/profile/')
        self.assertTrue(User.objects.filter(username='insinger').exists())
    def tearDown(self):
        Resident.objects.all().delete()
        User.objects.all().delete()

    def assertLoginFails(self, url, client=None):
        if client is None:
            client = Client()
            client.get('/login/')
        r = client.get(url)
        self.assertIn(b'Failure', r.content)

    @staticmethod
    def create_valid_login_url(email, client):
        r = client.get('/login/')
        token = parse_qs(urlparse(r.url).query)['token'][0]
        message = "{}:{}".format(token, email).encode('utf-8')
        h = hmac.new(settings.SCRIPTS_AUTH_KEY, message, hashlib.sha256)
        qs = urlencode({ 'email': email, 'signature': h.hexdigest() })
        return '/login/?{}'.format(qs)

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
