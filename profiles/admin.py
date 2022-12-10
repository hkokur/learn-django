from django.contrib import admin
from .models import Profile, Creator, Editor

admin.site.register(Profile)
admin.site.register(Creator)
admin.site.register(Editor)