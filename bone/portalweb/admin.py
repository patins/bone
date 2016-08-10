from django.contrib import admin
from .models import Tinder

class TinderAdmin(admin.ModelAdmin):
    list_display = ('resident', 'name', 'age', 'location')
    search_fields = ('name', 'location', 'bio')

admin.site.register(Tinder, TinderAdmin)
