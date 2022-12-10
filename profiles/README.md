# Summary

in profiles app, i have implemented profile approach for user authentication. Profiles app have 3 differen models and each of them is also a role for user. I make an effort to write everythig from scracth. For this reason, i don't use any advanced CBV. Views are inherited from View CBV. i also use forms.Form for every form. Log in, Log out, Update and Registration are performed without any mixins to make more configuratable.

With these views, i also cover how media files handle properly. I use FSS(FileSystemStorage) built-in django library. It is more appropriate way to handle media files.

# Model

I have 3 models :

- Profile
- Creator
- Editor

Profile have one-to-one relationship with CustomUser and also have profile_picture fields.

Creator and Editor have one-to-one realtionship with Profile.

# Forms

forms.FormModel is actually more appropriate to create a form about your models but i have chosen the forms.Form. So i have writen every field that i want to take from user.

**UserTypeForm** => This form uses to choice how i want to register. Acording to choosing, view redirect to proper view page.

**CreationCustomUserForm** => I also use built-in authentication form but i prefer to write from scratch.

**CreationProfileForm** => contains profile fields to creat a valid profile

**SalaryForm** => Salary field have in the Editor and Creator model. Normally we don't want that users decide himselft salary but i don't wrtite any manager so i have left at that.

**LoginForm** => It include necessary information fields(email and password).

# Views

we have 5 views.

**Main** => View decide where user shoul go. If he have profile, redirect him to update view. If he don't have any profile, then send the form to select registration type(user type).

    POST : Take user selection form sended form and redirect user to proper registration stage

**Registration** =>

    GET : Firstly, it look what's aim. According to that, it send proper form to user. It uses hierarchy to determine which form is proper. It uses different form for each stage of registration.

    POST :  According to hierarchy that GET method create, information that send via form save to database. With this implementation, i have aimed to create a  user that can have role with partial form but also i have not want to save faulty user information to database.

**Login** => Send LoginForm via get method and with post method, use authenticate and login function to log in properly.

**Logout** => uses logout function and redirect user to login page

**Update =>** This is most important view with registration view.

    GET : According to user role, create the forms that imported from forms.py. After that, prepopulate the area with current information.

    POST : User can send only one form each time so i determine the form that sended with name of submit button. According to that, i update the current information with new information if form is valid. Through the process, i use request to determine user himself.
