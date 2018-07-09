from django.conf.urls import url
import djangle.views as views

urlpatterns = [
    url(r'^', views.home, name='home'),
]
