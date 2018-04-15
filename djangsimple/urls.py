from django.conf.urls import url
import djangsimple.views as views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
