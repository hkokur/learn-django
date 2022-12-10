
from django import forms
from accounts.models import CustomUser
from .models import (
    Profile
)


# Selection Form to select type of user that want to register
class UserTypeForm(forms.Form):
    USER_TYPE = (
        ('CU','Common User'),
        ('CR','Creator'),
        ('ED', 'Editor')
    )
    user_types = forms.ChoiceField(choices=USER_TYPE, label='User Types', widget= forms.widgets.RadioSelect)


# Creation form for Custom User Model
class CreationCustomUserForm(forms.Form):
    username = forms.CharField(label='Username' , max_length= 150)
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(
        label= 'Password',
        max_length=150, 
        widget = forms.PasswordInput(
            attrs= {
                'placeholder' : 'Password',
            }
        )
    )


# Creation form for profile 
class CreationProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length = 200)
    age = forms.IntegerField(label='Your Age', min_value=0, max_value = 32767)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)


# set the salary of editor or creator
class SalaryForm(forms.Form):
    salary = forms.IntegerField(label='Salary')


# Login form 
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput())

