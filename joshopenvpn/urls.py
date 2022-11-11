from django.urls import include, path
from django.contrib import admin
from django.views import generic
from joshopenvpn.views import create, revoke

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create', create, name='create'),
    path('api/revoke', revoke, name='revoke')
]
