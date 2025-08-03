from django.contrib import admin

from .models import Area, Camera, DetectionEvent, PpeClass, Site

admin.site.register(Site)
admin.site.register(Area)
admin.site.register(Camera)
admin.site.register(PpeClass)
admin.site.register(DetectionEvent)
