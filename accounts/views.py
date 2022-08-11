from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    UpdateView,
    )
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class MainView(TemplateView):
    template_name = "registration/main.html"


class UpdateProfileView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "registration/profile_update.html"
    success_url = reverse_lazy('accounts')

    def test_func(self):
        obj = self.get_object()
        return obj.username == str(self.request.user)