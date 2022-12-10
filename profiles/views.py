from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from .forms import (
    UserTypeForm,
    CreationCustomUserForm,
    CreationProfileForm,
    SalaryForm,
    LoginForm,
)
from accounts.models import CustomUser 
from .models import (
    Profile,
    Creator,
    Editor,
)


class Main(View):
    """
        Main View that determine what's next page for user
    """
    template_name = 'profiles/main.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # check the user wheter he has a profile or not
        if hasattr(user, 'profile'):
            return HttpResponseRedirect(reverse('profile-update'))
        context = {
            'form' : UserTypeForm(),
        }
        return render(self.request, self.template_name, context)

    def post(self,request, *args, **kwargs):
        form = UserTypeForm(request.POST)
        goal = 0
        # set goal to determine the step of the registration
        # goal = 0 for basic registration but i don't include these choice in the form
        # gaol = 1 for creating a basic account and also creating a profile 
        # goal = 2 for creating creator role
        # goal = 3 for creating editor role
        if form.is_valid():
            user_type = form.cleaned_data['user_types']
            if user_type == "CU":
                return HttpResponseRedirect(reverse('profile-registration', args= [1]))
            elif user_type == 'CR':
                return HttpResponseRedirect(reverse('profile-registration', args=[2]))
            elif user_type == 'ED':
                return HttpResponseRedirect(reverse('profile-registration', args=[3]))         
        else :
            return HttpResponseRedirect(reverse("profile-main"))


class Registration(View):
    """
        Registration proccess acording to your goal. You can register for 3 different role in one view.
    """
    template_name = 'profiles/signup.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        context = {}
        goal = kwargs['goal']

        # if user don't have any account, return creation form 
        if not user.is_authenticated:
            context['form'] = CreationCustomUserForm()
            return render(self.request, self.template_name, context)
        
        if goal < 1:
            return HttpResponseRedirect(reverse("accounts"))
        
        # sending creation profile form
        if not hasattr(user, 'profile'):
            form = CreationProfileForm()
            del form.fields['profile_picture']
            context['form'] = form
            return render(self.request, self.template_name, context)

        if goal < 2:
            return HttpResponseRedirect(reverse("profile-update"))
        
        if not hasattr(user.profile, 'editor') or not hasattr(user.profile, 'creator'):
            context['form'] = SalaryForm()
            return render(self.request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse("profile-update"))

    def post(self, request, *args, **kwargs):
        user = self.request.user
        goal = kwargs['goal']

        if not user.is_authenticated:
            form = CreationCustomUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = CustomUser.objects.create_user(email, password, username=username)
                    user.save()
                    login(self.request, user)
                except IntegrityError:
                    context = {}
                    form.add_error('email', 'email and username must be uniqe!')
                    context['form'] = CreationCustomUserForm(form.cleaned_data)
                    return render(self.request, self.template_name, context)
            if goal != 0:
                return HttpResponseRedirect(reverse('profile-registration',  args=[goal]))
            else:
                # end the registration process and redirect to accounts page
                return HttpResponseRedirect(reverse("accounts"))

        # we have sent profile form if user don't have profile
        if not hasattr(user, 'profile'):
            form = CreationProfileForm(request.POST)
            if form.is_valid():
                profile = Profile.objects.create(
                    user=user,
                    **form.cleaned_data
                )
                profile.save()
            if goal != 1:
                return HttpResponseRedirect(reverse('profile-registration', args=[goal]))
            else:
                # if goal is 1 then, stop registration proccess and redirect to update page
                return HttpResponseRedirect(reverse("profile-update"))
        
        if goal == 2 or goal == 3:
            form = SalaryForm(request.POST)
            if form.is_valid():
                if goal == 2:
                    creator = Creator.objects.create(
                        profile=user.profile,
                        salary=form.cleaned_data['salary']
                    )
                    creator.save()
                elif goal == 3:
                    editor = Editor.objects.create(
                        profile=user.profile,
                        salary=form.cleaned_data['salary']
                    )
                    editor.save()
                return HttpResponseRedirect(reverse("profile-update"))
            else:
                return HttpResponseRedirect(reverse('profile-registration', args=[goal]))
                
        
class Login(View):
    """
        A login page have been written from scratch. Used the basic forms with basic view. 
    """
    template_name = 'profiles/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = LoginForm()
        return render(self.request, self.template_name, context )
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            if user is not None:
                login(self.request, user)
                return HttpResponseRedirect(reverse('proofile-main'))
            form.add_error('email', 'Please, enter valid email and password.')
        context = {
            'form' : form
        }
        return render(self.request, self.template_name, context)


class Logout(View):
    """
        Basic logout view
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(self.request)
        return HttpResponseRedirect(reverse('profile-login'))


class Update(View):
    """
    Update view that update user, profile etc. information. User can edit any information that realated about him.
    To achive this proccess, i use the forms that inherit from forms.Form. I had have multiple form to handle in one view so i use name attribute with button html tag. 
    """
    template_name = 'profiles/update.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}
        # add user role selection form to change role if user want
        context['role_form'] = UserTypeForm()

        if user.is_authenticated:
            form = CreationCustomUserForm(
                {
                    "username" : user.username,
                    "email" : user.email,
                }
            )
            del form.fields['password']
            form.add_error('username', 'email and username must be unique!')
            context['user_form'] = form
        else:
            return HttpResponseRedirect(reverse('profile-login'))
        
        if hasattr(user, 'profile'):
            context['profile_form'] = CreationProfileForm(
                {
                    "first_name" : user.profile.first_name,
                    "last_name" : user.profile.last_name,
                    "age" : user.profile.age,
                }

            )
            if hasattr(user.profile, 'creator'):
                context['salary_form'] = SalaryForm(
                    {
                        "salary" : user.profile.creator.salary
                    }
                )
            elif hasattr(user.profile, 'editor'):
                context['salary_form'] = SalaryForm(
                    {
                        'salary' : user.profile.editor.salary
                    }
                )
        else:
            return HttpResponseRedirect(reverse('profile-main'))

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        user = request.user

        # update custom user informations
        if 'user_form' in request.POST:
            form = CreationCustomUserForm(request.POST)
            del form.fields['password']
            if form.is_valid():
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                try:
                    user.save()
                except IntegrityError:
                    pass

        # update profile informations
        if 'profile_form' in request.POST:
            print(request.FILES)
            form = CreationProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = user.profile
                picture = form.cleaned_data['profile_picture']
                # update profile picture with File System Storage
                if picture is not None:
                    fss = FileSystemStorage()
                    if profile.profile_picture is not None and profile.profile_picture != "":
                        fss.delete(profile.profile_picture.name)
                    name = fss.save('profile_pictures/' + picture.name , picture)
                    form.cleaned_data['profile_picture'] = name
                else:
                    del form.cleaned_data['profile_picture']
                Profile.objects.filter(uuid = profile.uuid).update(
                    **form.cleaned_data
                )

        # update editor or creator salary       
        if 'salary_form' in request.POST:
            form = SalaryForm(request.POST)
            if form.is_valid():
                if hasattr(user.profile, 'creator'):
                    Creator.objects.filter(profile=user.profile).update(
                        **form.cleaned_data
                    )
                elif hasattr(user.profile, 'editor'):
                    Editor.objects.filter(profile=user.profile).update(
                        profile=user.profile,
                        **form.cleaned_data
                    )

        # update user role 
        if 'role_form' in request.POST:
            form = UserTypeForm(request.POST)
            if form.is_valid():
                user_type = form.cleaned_data['user_types']
                if user_type == "CU":
                    if hasattr(user.profile, 'creator'):
                        user.profile.creator.delete()
                    elif hasattr(user.profile, 'editor'):
                        user.profile.editor.delete()

                if user_type == 'CR':
                    if not hasattr(user.profile, 'creator') and not hasattr(user.profile, 'editor'):
                        return HttpResponseRedirect(reverse('profile-registration', args=[2]))
                    elif hasattr(user.profile, 'editor'):
                        creator = Creator.objects.create(
                            profile= user.profile,
                            salary= user.profile.editor.salary
                        )
                        user.profile.editor.delete()

                if user_type == 'ED':
                    if not hasattr(user.profile, 'creator') and not hasattr(user.profile, 'editor'):
                        return HttpResponseRedirect(reverse('profile-registration', args=[3]))
                    elif hasattr(user.profile, 'creator'):
                        editor = Editor.objects.create(
                            profile= user.profile,
                            salary= user.profile.creator.salary
                        )
                        user.profile.creator.delete()

        return HttpResponseRedirect(reverse('profile-update'))