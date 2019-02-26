from django.contrib import admin
from .models import Event, Announcement, EventAnnouncement
# Register your models here.
admin.site.register(Event)
admin.site.register(Announcement)
admin.site.register(EventAnnouncement)


