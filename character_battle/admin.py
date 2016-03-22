from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Attribute)
admin.site.register(Character)
admin.site.register(Challenge)
admin.site.register(Battle)