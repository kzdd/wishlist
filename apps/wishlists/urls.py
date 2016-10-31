from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create$', views.create, name='create'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^addproduct/(?P<id>\d+)$', views.addproduct, name='addproduct'),
    url(r'^removeproduct/(?P<id>\d+)$', views.removeproduct, name='removeproduct'),
    url(r'^product/(?P<id>\d+)$', views.product, name='product'),
]
