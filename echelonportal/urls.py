"""echelonportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tracker import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^editproject', views.editproject, name='editproject'),
    url(r'^checkproject', views.checkproject, name='checkproject'),
    url(r'^deleteproject', views.deleteproject, name='deleteproject'),
    url(r'^addproject', views.addproject, name='addproject'),
    url(r'^addcredits', views.addcredits, name='addcredits'),
    url(r'^signout', views.signout, name='signout'),
    url(r'^credits', views.credits, name='credits'),
    url(r'^newuser', views.createnewuser, name='createnewuser'),
    url(r'^signedin', views.viewuserdata, name='viewuserdata'),
]
