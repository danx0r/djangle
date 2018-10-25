from django.conf.urls import url
import djserver.views as views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^api_login$', views.login, name='login'),
    url(r'^api_logout$', views.logout, name='logout'),
    url(r'^whoami$', views.whoami, name='whoami'),
    url(r'^files/', views.files, name='files'),
    url(r'^static/', views.static, name='files'),
    url(r'^', views.home, name='home'),
]
