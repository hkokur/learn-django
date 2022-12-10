# Summary

This is my implementation repository for django. My purpose is build app to understand well django concepts such as generic-class-view, authentication, messages framework etc. Each app have own readme file and i explain what my aim for the app. Below brief list of purpose of apps.

blog : basic CRUD sytem with class-based and function-based view

account : basic custom auth system include sign up, login, logout, edit profile and changing password.

profiles: I have made effort with the app to dive more deep about views and forms. So i uses only View(CBV) class and Form(forms.Form) to handle any action. With the app, user can have a profile with profile pciture, first name, age etc. So the app includes file handling with FileSystemStorage and other field update process. Also user can have 2 different role(creator and editor).

authorization: The app is focused the permission concepts. Actually django give us two way to restrict the actions by users: permissions and groups. Permissions are more straightforwad but also more challenging when trying to give a permission to several users. Because of that,  the app is more about group. Permissions is created and added to proper group but don't implement individually.

You can visit https://learn-djang0.herokuapp.com/ to see implementations.

(Important Note: I have set the debug to True, in production it is deathful mistake but in my stuation, it is necessary to serve media files. I don't use nginx with heroku or 3rd library like django-storage so i can't find more ideal solution for now.)
