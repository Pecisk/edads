from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Advertisement, Station, StarSystem, Commander, Tradeable

admin.site.register(User, UserAdmin)
admin.site.register(Advertisement)
admin.site.register(Commander)
admin.site.register(Tradeable)