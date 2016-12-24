from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^login', views.login, name = 'login'),
    url(r'^signup', views.signup, name = 'signup'),
    url(r'^newuser', views.createnewuser, name = 'createnewuser'),
    url(r'^signedin', views.viewuserdata, name = 'viewuserdata'),
    #url(r'^createnewuser', views.createnewuser, name = 'createnewuser'),
    #url(r'^/user/(?P<UserID>[a-z0-9]+)',views.user, name = 'user'),
]