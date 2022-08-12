# Summary
In this section, my purpose have performed CRUD implementation. When i have been implementing, i have apoted both two aproach, function-based and class-based view. When i have said class-based view, i have refered to generic-class-based view because writing class from scracth to perform CRUD is slow and also django provide us well predefined classes. 

# Function-Based View
C => I have created a form(you can see in form.py) to take data from user. i have sent empty form to user when i have taken GET request. User have sent filled form via POST request and i have checked wheter all value is valid or not. If all value have been valid, add user that logined user or none and save form to database, redirect detail view of page created.

R => GET : get object with slug from database and return detail view.

U => GET : get object with slug from database and fill form with object. This filled form send to user. 
    POST : fill form via POST elements. check all value is valid.  if all fo them are valid, add user and save to database, redirect to detail view.

D => GET : get object with slug and send a form to confirm deletion.
    POST : delete object and redirect to pagination page. 

Also, if you click CRUD links on pagination page, it get random object from database.

# Class-Based View
C =>  I have used the CreateView. i haven't defined get_absolute_url in model, so i have configured the get_succes_url. Createview use get_absolute_url method to 
    redirect after creation. 

R => I have used the DetailView. I have configured the get_object method to return random object when requested.

U => I have used the UpdateView and configured the get_object again. 

D => I have used the DeleteView and configured the get_object again. 

Also, if you click CRUD links on pagination page, it get random object from database.
