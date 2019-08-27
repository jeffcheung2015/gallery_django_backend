from django.contrib import admin
from .models import Image, Tag, Profile, Activity
# Register your models here.
admin.site.register([Image, Tag, Profile, Activity])
