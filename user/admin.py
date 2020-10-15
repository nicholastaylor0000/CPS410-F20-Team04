from django.contrib import admin
from .models import UserProfile, PassReset

admin.site.register(UserProfile)
admin.site.register(PassReset)
