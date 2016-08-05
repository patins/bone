from django.test import TestCase
from django.test import Client
from .models import Resident, REXEvent
from datetime import datetime, timedelta
from django.utils import timezone

def the_past():
    return timezone.now() - timedelta(hours=1)

def the_future():
    return timezone.now() + timedelta(hours=1)

class HomePageTestCase(TestCase):
    def setUp(self):
        self.c = Client()
    def test_home(self):
        r = self.c.get('/')
        self.assertIn(b"Welcome", r.content)
        self.assertEqual(200, r.status_code)
        self.assertNotIn(b"REX Events", r.content)
    def test_home_rex_events(self):
        REXEvent.objects.create(name="Pat's Test Event", start=the_past(), end=the_future(), visible=True)
        REXEvent.objects.create(name="NOTVISIBLE Event", start=the_past(), end=the_future())
        REXEvent.objects.create(name="LATE Event", start=the_past(), end=the_past(), visible=True)
        r = self.c.get('/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b"REX Events", r.content)
        self.assertNotIn(b"NOTVISIBLE", r.content)
        self.assertNotIn(b"LATE", r.content)
        REXEvent.objects.all().delete()

class StaticPageTestCase(TestCase):
    def setUp(self):
        self.c = Client()
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
        Resident.objects.create(name='Anubhav', kerberos='ajain', year=2016, visible=True, alumni=True)
    def test_main_page(self):
        r = self.c.get('/residents/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
        self.assertIn(b'Shader', r.content)
        self.assertNotIn(b'Anubhav', r.content)
    def test_2019_page(self):
        r = self.c.get('/residents/2019/')
        self.assertEqual(200, r.status_code)
        self.assertIn(b'Patrick', r.content)
        self.assertIn(b'Abhi', r.content)
        self.assertNotIn(b'Shader', r.content)
        self.assertNotIn(b'Anubhav', r.content)
    def test_2018_page(self):
        r = self.c.get('/residents/2018/')
        self.assertEqual(200, r.status_code)
        self.assertNotIn(b'Patrick', r.content)
        self.assertNotIn(b'Abhi', r.content)
        self.assertIn(b'Shader', r.content)
        self.assertNotIn(b'Anubhav', r.content)
    def test_2016_page(self):
        r = self.c.get('/residents/2016/')
        self.assertEqual(200, r.status_code)
        self.assertNotIn(b'Patrick', r.content)
        self.assertNotIn(b'Abhi', r.content)
        self.assertNotIn(b'Shader', r.content)
        self.assertIn(b'Anubhav', r.content)
    def test_alumni_page(self):
        r = self.c.get('/residents/alumni/')
        self.assertEqual(200, r.status_code)
        self.assertNotIn(b'Patrick', r.content)
        self.assertNotIn(b'Abhi', r.content)
        self.assertNotIn(b'Shader', r.content)
        self.assertIn(b'Anubhav', r.content)

    def tearDown(self):
        Resident.objects.all().delete()

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
