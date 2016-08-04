from django.contrib import admin
from .models import Resident

def make_hidden(modeladmin, request, queryset):
    queryset.update(visible=False)
make_hidden.short_description = "Hide selected residents"

def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)
make_visible.short_description = "Show selected residents"

class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'kerberos', 'year', 'bio', 'visible')
    list_filter = ('year', 'visible')
    search_fields = ('name', 'kerberos')
    actions = [make_hidden, make_visible]

admin.site.register(Resident, ResidentAdmin)
