from django.conf.urls import url

from . import views

app_name = 'reports'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<pk>[0-9]+)/asn/$', views.ASNDetail.as_view(), name='asnDetail'),
    url(r'^monitoredAsn/$', views.ASNList.as_view(), name='asnList'),
    url(r'^data/congestion/$', views.congestionData, name='congestionData'),
    url(r'^data/forwarding/$', views.forwardingData, name='forwardingData'),
]
