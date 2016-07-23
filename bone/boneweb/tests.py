from django.test import TestCase
from django.test import Client

from .models import Resident

class StaticPageTestCase(TestCase):
    def setUp(self):
        self.c = Client()
    def test_home(self):
        r = self.c.get('/')
        self.assertIn(b"Welcome", r.content)
        self.assertEqual(200, r.status_code)
    def test_about(self):
        r = self.c.get('/about/')
        self.assertIn(b"About", r.content)
        self.assertEqual(200, r.status_code)

class ResidentsPageTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        Resident.objects.create(name='Patrick', kerberos='insinger', year=2019, visible=True)
        Resident.objects.create(name='Abhi', kerberos='aveni', year=2019, visible=True)
        Resident.objects.create(name='Shader', kerberos='sshader', year=2018, visible=True)
    def test_main_page(self):
        r = self.c.get('/residents/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
        self.assertIn(b'Shader', r.content)
    def test_2019_page(self):
        r = self.c.get('/residents/2019/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
        self.assertNotIn(b'Shader', r.content)
    def test_2018_page(self):
        r = self.c.get('/residents/2018/')
        self.assertEqual(200, r.status_code)
        self.assertNotIn(b'Patrick', r.content)
        self.assertNotIn(b'Abhi', r.content)
        self.assertIn(b'Shader', r.content)
    def tearDown(self):
        Resident.objects.all().delete

class ResidentVisibilityTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        Resident.objects.create(name='Patrick', kerberos='insinger', year=2019, visible=False)
        Resident.objects.create(name='Abhi', kerberos='aveni', year=2019, visible=True)
    def test_main_page_visibility(self):
        r = self.c.get('/residents/')
        self.assertNotIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
    def test_year_page_visibility(self):
        r = self.c.get('/residents/2019/')
        self.assertNotIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
    def tearDown(self):
        Resident.objects.all().delete()
