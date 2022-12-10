from django.urls import path
from .views import (
    Main,
    Registration,
    Login,
    Logout,
    Update,
)


urlpatterns = [
    path('', Main.as_view(), name = 'profile-main'),
    path("signup/<int:goal>", Registration.as_view(),name = 'profile-registration'),
    path('login/', Login.as_view(), name='profile-login'),
    path('logout/', Logout.as_view(), name = 'profile-logout'),
    path('update/', Update.as_view(), name = 'profile-update'),
]