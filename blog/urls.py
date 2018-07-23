"""medium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from blog import views

urlpatterns = [
    url('posts/create', views.create_post, name="posts_create"),
    url(r'^posts/delete/(?P<pk>\d+)$', views.delete_post, name="posts_delete"),
    url(r'^posts/edit/(?P<pk>\d+)$', views.update_post, name="posts_edit"),
    url(r'^posts/(?P<pk>\d+)$', views.post_detail, name="posts_details"),
    url('posts', views.list_post, name="posts_list"),
]
