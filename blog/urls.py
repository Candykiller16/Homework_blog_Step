from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag')
]
