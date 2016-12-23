from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^signedin', views.viewuserdata, name = 'viewuserdata'),
    #url(r'^/user/(?P<UserID>[a-z0-9]+)',views.user, name = 'user'),
]