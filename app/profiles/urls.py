from django.conf.urls import url, patterns, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^success/$', views.success, name='success'),
	url(r'^all/$', views.ProfileView.as_view(), name='all'),
]