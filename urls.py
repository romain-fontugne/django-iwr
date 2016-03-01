from django.conf.urls import url

from . import views

app_name = 'reports'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<pk>[0-9]+)/asn/$', views.ASNView.as_view(), name='asnDetail'),
    url(r'^data/congestion/$', views.congestionData, name='congestionData'),
    url(r'^data/forwarding/$', views.forwardingData, name='forwardingData'),
]
