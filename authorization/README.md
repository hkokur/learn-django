# Summary

The app propose ise the implemention authorization concepts with proper aproach. I create 5 different groups for 3 type of roles. User can easy change your own group or can change role from profiles app. Each group have special permissions. These permissions and groups create or get through group selection stage. Proper permissions are added to group and this group also is added to a user.

So user include a selected group and also have permission for some action. Hence, i have two options to give acces to perform action, groups or permissions. I have chose second one, group. It is more sensible for my stuation but also permissions can been use.

I have explained the groups and their permissions details in authorization main page.

# Models

I have 2 models, post and review. Actually they are mimic models themself. They are same field except post field in review model. Post model is straigthforwad. Its fields : **uuid, slug, updated_at, published_at, status, title, author, content**. Proper user can change some fields. Review app have same fields and post fields. If you are in review_creators, you can write any number of reviews about any posts.

# Forms

i have 2 forms. One of them is to change group and another one is a model form for post creation.

ChangeGroupForm => It includes possible group choices. User can select him group via this form.

PostCreationForm => A model form to create a post. No advance customization. It have model and fields fields in meta class.

# Views

We have 3 roles(user, creator and editor) and 5 groups(post_creators, review_creator, post_editors, review_editors, special_users). User must be editor to attempt the editors group or must be creator to attempt the creators group. Everyone that have profile can attemp the special user group.  

Editors can edit content or meta data acording to their types, same as the creators. Special users have a uniqe permission to delete any post permanately.

Before return any responses, check whether user is in the proper group to perform the action that user requested. 

**MainView =>** return post and review list. if user don't authenticate, he can only see published reviews or posts.

**ChangeGroupView =>** 

    GET :  return a selection form so that user select own group.

    POST : The method firstly check the form is valid or not. When form is valid, delete group that user have and start to process to add to new group. Create content types and create or get permissions. Acording to choice that user send with form, create or get the proper group and add the user to this group. If user don't have proper qualification, sends back the warning message.

**PostCreationView =>** 
    GET : The method uses the PostCreationForm that is model form but delete author field. This field is field up with user that log in.

    POST : Get information from request object and create new valueDict with current user(also creator). If fom is invalid, return the current form with prepopulated fields.

**ReviewCreationView =>** The view is inherited from CreatView so i just have configurated the form.instance.author field with current user. 

**PostDetailView, PostUpdateMetaView, PostUpdateContentView, PostDeleteView, ReviewDetailView, ReviewUpdateMetaView, ReviewUpdateContentView, ReviewDeleteView =>** All of these view are inherited from predefined CBV like DetailView or UpdateView. So I have handled with minimum effort the actions. To perform some action, need some previliges. I have checked the previliges with UserPassesTestMixin.
