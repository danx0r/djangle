from django.conf.urls import url
import djserver.views as views

urlpatterns = [
    url(r'^', views.home, name='home'),
]
