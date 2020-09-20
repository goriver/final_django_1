"""web_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import include, path
from blog.views import post_list
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views
from blog.views import post_list, post_detail, post_add, post_delete, post_publish, graph, wordcloud, search, search_result, moreinfo, moreinfo_out
from django.urls import path


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list, name = 'home'),  # url 객체를 만들어준다.
    url(r'^post/(?P<pk>\d+)/', post_detail), 
    url(r'^post/add/$', post_add, name='post_add'),
    url(r'^post/(?P<pk>\d+)/delete/$', post_delete, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/publish/$', post_publish, name='post_publish'),
    url(r'^post/search/', search, name='search'),
    url(r'^post/search_result/', search_result, name='search_result'), # (?P<slug>[-\w]+) 문자열 
    url(r'^post/graph/', graph, name='graph'),
    url(r'^wordcloud/', wordcloud, name="wordcloud"),
    url(r'^post/moreinfo/', moreinfo, name="moreinfo"),
    url(r'^post/moreinfo_out/', moreinfo_out, name="moreinfo_out"),

    
]