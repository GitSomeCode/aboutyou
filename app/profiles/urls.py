from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^success/$', views.success, name='success'),
    url(r'^explore/$', views.ProfileList.as_view(), name='all'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^(?P<slug>[-\w]+)/$', views.ProfileView.as_view(), name='profile_view'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.profile_update, name='profile_update'),
    url(r'^(?P<slug>[-\w]+)/editform/$', views.ProfileUpdate.as_view(), name='profile_update_form'),
]
