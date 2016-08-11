from django.test import TestCase
from django.test import Client

from boneweb.models import Resident, Quote
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

class QuotesPrivateTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='insinger')
        pat = Resident.objects.create(
            name='Patrick',
            kerberos='insinger',
            year=2019,
            user=user
        )
        abhi = Resident.objects.create(name='Abhi', kerberos='aveni', year=2019, visible=True)
        Quote.objects.create(text="Funnels everyday", author=pat, submitter=abhi, public=True)
        Quote.objects.create(text="Never forget the 3-week rule", author=abhi, submitter=abhi, public=False)
        self.c = Client()
        self.c.force_login(user)
    def test_new_quote_page(self):
        r =  self.c.get('/quotes/new/')
        self.assertEqual(200, r.status_code)
    def test_submit_new_quote(self):
        r = self.c.post('/quotes/new/', {'text': "Ciroc dons", 'author' : Resident.objects.get(name="Abhi").id, 'public' : True})
        self.assertEqual(302, r.status_code)
        self.assertEqual('Patrick', Quote.objects.get(text="Ciroc dons").submitter.name)
        r = self.c.get('/quotes/')
        self.assertIn(b"Ciroc dons", r.content)
    def test_quotes_private_viewability(self):
        r = self.c.get('/quotes/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b"Funnels everyday", r.content)
        self.assertIn(b"Never forget the 3-week rule", r.content)
    def tearDown(self):
        Resident.objects.all().delete()
        User.objects.all().delete()
        Quote.objects.all().delete()