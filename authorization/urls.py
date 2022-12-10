from django.urls import path
from .views import (
    MainView,
    ChangeGroupView,
    PostCreationView,
    ReviewCreationView,
    PostDetailView,
    PostUpdateMetaView,
    PostUpdateContentView,
    PostDeleteView,
    ReviewDetailView,
    ReviewUpdateMetaView,
    ReviewUpdateContentView,
    ReviewDeleteView,
)


urlpatterns = [
    path('', MainView.as_view(), name='authorization-main'),
    path('change-group/', ChangeGroupView.as_view(), name='authorization-group'),
    path('add-post/', PostCreationView.as_view(), name='authorization-add-post'),
    path('add-review/', ReviewCreationView.as_view(), name= 'authorization-add-review'),
    path('post/<slug:slug>-<uuid:uuid>', PostDetailView.as_view(), name='authorization-detail-post'),
    path('post/update-meta/<uuid:uuid>', PostUpdateMetaView.as_view(), name='authorization-meta-post'),
    path('post/update_content/<uuid:uuid>', PostUpdateContentView.as_view(), name='authorization-content-post'),
    path('post/delete/<uuid:uuid>', PostDeleteView.as_view(), name='authorization-delete-post'),
    path('review/<slug:slug>-<uuid:uuid>', ReviewDetailView.as_view(), name='authorization-detail-review'),
    path('review/update-meta/<uuid:uuid>', ReviewUpdateMetaView.as_view(), name='authorization-meta-review'),
    path('review/update_content/<uuid:uuid>', ReviewUpdateContentView.as_view(), name='authorization-content-review'),
    path('review/delete/<uuid:uuid>', ReviewDeleteView.as_view(), name='authorization-delete-review'),
]