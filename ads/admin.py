from django.contrib import admin

from .models import User, Cat, Location, Ads

admin.site.register(Location)
admin.site.register(Ads)
admin.site.register(Cat)
admin.site.register(User)