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
from home import views as views1
from tracker import views as views2
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views1.index,name = 'home'),
    url(r'^login', views2.login, name = 'login'),
    url(r'^signup', views2.signup, name = 'signup'),
    url(r'^newuser', views2.createnewuser, name = 'createnewuser'),
    url(r'^signedin', views2.viewuserdata, name = 'viewuserdata'),
]
