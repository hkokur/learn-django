from django.urls import path
from .views import HomePage, BlogPagination, blog_pagination, blog_main


urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("blog/",blog_main, name="blog"),
    path("blog/c-<int:page>/", BlogPagination.as_view(), name="class_pagination"),
    path("blog/<int:page>/", blog_pagination, name="func_pagination"),
]