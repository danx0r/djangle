from django.conf.urls import url
import djserver.views as views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^whoami$', views.whoami, name='whoami'),
    url(r'^', views.home, name='home'),
]
