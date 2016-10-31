from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'login'),
    url(r'^process$', views.process, name = 'process'),
    url(r'^logout$', views.logout, name = 'logout')
]
