from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admin/$', views.index, name = 'index'),
    url(r'register/$', views.register, name = 'register'),
    url(r'login/$', views.login, name = 'login'),
    url(r'logout/$', views.logout, name = 'logout'),
    url(r'create_new/$', views.create_new, name = 'create_new'),
]