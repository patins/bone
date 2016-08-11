from django.contrib import admin
from .models import Resident, REXEvent, Quote

def visible_actions(model):
    def make_hidden(modeladmin, request, queryset):
        queryset.update(visible=False)
    make_hidden.short_description = "Hide selected {}".format(model._meta.verbose_name_plural)

    def make_visible(modeladmin, request, queryset):
        queryset.update(visible=True)
    make_visible.short_description = "Show selected {}".format(model._meta.verbose_name_plural)

    return [make_hidden, make_visible]

def make_alumni(modeladmin, request, queryset):
    queryset.update(alumni=True)
make_alumni.short_description = "Graduate selected residents"

def make_current(modeladmin, request, queryset):
    queryset.update(alumni=False)
make_current.short_description = "Fail selected residents"

class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'kerberos', 'year', 'bio', 'visible', 'alumni')
    list_filter = ('year', 'visible', 'alumni')
    search_fields = ('name', 'kerberos')
    actions = visible_actions(Resident)
    actions.extend([make_alumni, make_current])

admin.site.register(Resident, ResidentAdmin)

class REXEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'description', 'location', 'visible')
    list_filter = ('visible',)
    search_fields = ('name', 'description', 'location')
    actions = visible_actions(REXEvent)

admin.site.register(REXEvent, REXEventAdmin)

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_quote', 'author', 'submitter', 'public', 'visible')
    list_filter = ('author', 'public', 'visible')
    search_fields = ('text', 'author', 'submitter')
    actions = visible_actions(Quote)

admin.site.register(Quote, QuoteAdmin)
