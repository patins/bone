
MENU_ITEMS = [
    ('home', "Home"),
    ('about', "About"),
    ('residents', "Residents"),
]

def menu(request):
    return {
        'menu': MENU_ITEMS
    }
