"""manatwee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from twttr.views import NetworkListView, ShowListView, ShowDetailView, HomeListView,AboutListView, ContactListView,homeviewfunc, aboutviewfunc, contactviewfunc,showdetailfunc,AutoCompleteView, search_func
from critic.views import movieviewfunc
from django.contrib.auth.views import login, logout
from accounts.views import register_view_func

#from twttr.views import HomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',homeviewfunc),
    url(r'^about/$',aboutviewfunc),
    url(r'^contact/$',contactviewfunc),
    url(r'^network/$',NetworkListView.as_view()),
    url(r'^show/(?P<slug>[\w-]+)/$',showdetailfunc,name='showdetailfunc'),
    url(r'^autocomplete/$',AutoCompleteView.as_view(), name='autocomplete'),
    url(r'^search/$', search_func, name='search_func'),
    url(r'^login/$', login,{'template_name':'Acct/login.html'}),
    url(r'^logout/$',logout,{'template_name':'Acct/logout.html'}), 
    url(r'^register/$',register_view_func,name='registry page'), 

]
