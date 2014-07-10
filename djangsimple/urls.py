from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'djangsimple.views.home', name='home'),
)
