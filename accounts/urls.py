from django.urls import path

from .views import (
    SignUpView,
    MainView,
    UpdateProfileView
    )

urlpatterns = [
    path("", MainView.as_view(), name='accounts'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("update/<int:pk>", UpdateProfileView.as_view(), name="update_profile"),
]