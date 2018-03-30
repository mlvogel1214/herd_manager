from django.conf.urls import url 
from . import views
urlpatterns = [
    url(r'^dashboard/$', views.index, name = 'dashboard'),
    url(r'^add/$', views.add, name = 'add'),
    url(r'^view/(?P<id>\d+)$', views.view, name = 'view'),
    url(r'^create/$', views.create, name = 'create'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'^addRelated/$', views.addOff, name = 'addRelated')
   
]