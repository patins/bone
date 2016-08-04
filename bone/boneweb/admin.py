from django.contrib import admin
from .models import Resident, REXEvent

def visible_actions(model):
    def make_hidden(modeladmin, request, queryset):
        queryset.update(visible=False)
    make_hidden.short_description = "Hide selected {}".format(model._meta.verbose_name_plural)

    def make_visible(modeladmin, request, queryset):
        queryset.update(visible=True)
    make_visible.short_description = "Show selected {}".format(model._meta.verbose_name_plural)

    return [make_hidden, make_visible]

class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'kerberos', 'year', 'bio', 'visible')
    list_filter = ('year', 'visible')
    search_fields = ('name', 'kerberos')
    actions = visible_actions(Resident)

admin.site.register(Resident, ResidentAdmin)

class REXEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'description', 'location', 'visible')
    list_filter = ('visible',)
    search_fields = ('name', 'description', 'location')
    actions = visible_actions(REXEvent)

admin.site.register(REXEvent, REXEventAdmin)
