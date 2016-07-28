from django.conf import settings


MENU_ITEMS = [
    ('home', "Home"),
    ('about', "About"),
    ('residents', "Residents"),
]

def menu(request):
    return {
        'menu': MENU_ITEMS
    }

def google_analytics(request):
    return {
        'GA_KEY': settings.GA_KEY
    }
