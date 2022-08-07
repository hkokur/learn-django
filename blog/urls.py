from django.urls import path
# Class-Based imports
from .views import (
    HomePage,
    BlogPagination,
    BlogDeatil,
    BlogCreate,
    BlogUpdate,
    BlogDelete,
    )
# Function-Based imports
from .views import (
    blog_main,
    blog_pagination,
    blog_create,
    blog_detail,
    blog_update,
    blog_delete,
    )


urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("blog/", blog_main, name="blog"),

    # Generic-Class Based
    path("blog/c/<int:page>/", BlogPagination.as_view(), name="class_pagination"),
    path("blog/c/new/", BlogCreate.as_view(), name="class_create"),
    path("blog/c/post/<slug:slug>/", BlogDeatil.as_view(), name="class_detail"),
    path("blog/c/update/<slug:slug>", BlogUpdate.as_view(), name="class_update"),
    path("blog/c/delete/<slug:slug>", BlogDelete.as_view(), name="class_delete"),

    # Function Based
    path("blog/f/<int:page>/", blog_pagination, name="func_pagination"),
    path("blog/f/new/", blog_create, name="func_create"),
    path("blog/f/post/<slug:slug>/", blog_detail, name='func_detail'),
    path("blog/f/update/<slug:slug>/", blog_update, name="func_update"),
    path("blog/f/delete/<slug:slug>", blog_delete, name="func_delete"),
]