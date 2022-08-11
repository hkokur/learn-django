# Summary 
in this section, i have implemented custom user model. Django recomend us that custom user model create before first migration. Otherwise, upgrading from default to custom is more difficult. I have crated custom model and setted setting.py configuration. After that django provide us much convenience like login, logout. With this shortcuts, i have builted basic sing up, login, logout, edit pasword and user information pages.

# Model
i have created CustomUserModel that inherite from AbstractUser. I have wanted to login with email so I have reassign username and emaile fields, changed USERNAME_FIELD from "username" (default) to "email". I have deleted first and last name field because i haven't wanted use them. in additon, I have reconfigured the default manager because of this altering necessarily.

# Form
CustomUserCreationForm => To add user to database. Thank to django, Parent handle password hashing, permission setting etc during creating. 
CustomUserChangeForm => It is for update some user attributes but doesn't include password changing.  

# View
SignUpView => Inherited from CreateView. Uses for sign up.
UpdateProfileView => Inherited from UpdateView and UserPassesTestMixin. It check user that want to edit attributes to understand whether user is itself or not before send form.

Other login, logout or password changing etc. views been handled by django. 