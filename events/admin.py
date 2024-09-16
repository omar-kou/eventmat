from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer')  # Assure-toi que 'organizer' est un champ valide

admin.site.register(Event, EventAdmin)
