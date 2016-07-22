from django.contrib import admin
from .models import Resident

class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'kerberos', 'bio', 'visible')

admin.site.register(Resident, ResidentAdmin)
