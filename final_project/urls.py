
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('character_battle.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
