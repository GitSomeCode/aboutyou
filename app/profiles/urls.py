from django.conf.urls import url, patterns, include
from django.contrib.auth.views import login
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^success/$', views.success, name='success'),
	url(r'^all/$', views.ProfileView.as_view(), name='all'),
	url(r'^login/$', views.custom_login, name='custom_login'),
	url(r'^logout/$', views.custom_logout, name='custom_logout'),

]