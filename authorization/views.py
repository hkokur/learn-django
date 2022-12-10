from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    View,
    ListView,
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import (
    Post, 
    Review,
    )
from .forms import (
    ChangeGroupForm,
    PostCreationForm
)


class MainView(TemplateView):
    """
    This view send all post and review acording to authenticate stuation. 
    Pagination is unnecessary so i don't use. 
    """
    template_name = 'authorization/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["all_posts"] = Post.objects.all()
            context['all_reviews'] = Review.objects.all()
        else:
            context["all_posts"] = Post.objects.filter(status='pub')
            context['all_reviews'] = Review.objects.filter(status='pub')
        return context


class ChangeGroupView(LoginRequiredMixin,TemplateView):
    """
    Get method sends form that user select group from
    Post method is major thing in here. It create or get content types or permissions. 
    It delete user current group and it assign new group to user with these special permissions. 
    """
    login_url = reverse_lazy('profile-login')
    template_name = 'authorization/change_group.html'

    def get(self, request, *args, **kwargs):
        form = ChangeGroupForm()
        kwargs['group_form'] = form
        return super().get(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        form = ChangeGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            user = request.user
            user.groups.clear()

            # content types
            ct_post = ContentType.objects.get_for_model(Post)
            ct_review = ContentType.objects.get_for_model(Review)

            # permissions
            edit_post = Permission.objects.get_or_create(
                        codename= 'edit_content',
                        name= 'Can edit content and title',
                        content_type=ct_post
                    )[0]
            edit_review = Permission.objects.get_or_create(
                        codename= 'edit_content',
                        name='Can edit content and title',
                        content_type=ct_review
                    )[0]
            meta_post = Permission.objects.get_or_create(
                        codename='edit_meta',
                        name='Can edit slug, status and publish date',
                        content_type=ct_post
                    )[0]
            meta_review = Permission.objects.get_or_create(
                        codename='edit_meta',
                        name='Can edit slug, status and publish date',
                        content_type=ct_review
                    )[0]
            create_post = Permission.objects.get_or_create(
                        codename='add',
                        name='Can add post',
                        content_type=ct_post
                    )[0]
            create_review = Permission.objects.get_or_create(
                        codename='add',
                        name='Can add post',
                        content_type=ct_review
                    )[0]
            delete_post = Permission.objects.get_or_create(
                        codename='delete',
                        name='Can delete post',
                        content_type=ct_post
                    )[0]
            delete_review = Permission.objects.get_or_create(
                        codename='delete',
                        name='Can delete post',
                        content_type=ct_review
                    )[0]

            if not hasattr(user, 'profile'):
                return HttpResponseRedirect(reverse('profile-main'))
            elif hasattr(user.profile, 'editor') and group.endswith('E'):
                if group == 'CE':
                    h_group = Group.objects.get_or_create(
                        name='content_editors',
                    )[0]
                    h_group.permissions.set(
                        (
                            edit_post, edit_review
                        )
                    )
                    user.groups.add(h_group)
                    return HttpResponseRedirect(reverse('authorization-main')) 
                elif group == 'ME':
                    h_group = Group.objects.get_or_create(
                        name='meta_editors',
                    )[0]
                    h_group.permissions.set(
                        (
                            meta_post, meta_review
                        )
                    )
                    user.groups.add(h_group)
                    return HttpResponseRedirect(reverse('authorization-main')) 
            elif hasattr(user.profile, 'creator') and group.endswith('C'):
                if group == 'PC':
                    h_group = Group.objects.get_or_create(
                        name='post_creators',
                    )[0]
                    h_group.permissions.set(
                        (
                            create_post,
                        )
                    )
                    user.groups.add(h_group)
                    return HttpResponseRedirect(reverse('authorization-main')) 
                elif group == 'RC':
                    h_group = Group.objects.get_or_create(
                        name='review_creators',
                    )[0]
                    h_group.permissions.set(
                        (
                        create_review,
                        )
                    )
                    user.groups.add(h_group)
                    return HttpResponseRedirect(reverse('authorization-main')) 
            elif group == 'SU':
                h_group = Group.objects.get_or_create(
                    name='special_users',
                )[0]
                h_group.permissions.set(
                    (
                        delete_post, delete_review
                    )
                )
                user.groups.add(h_group)
                return HttpResponseRedirect(reverse('authorization-main')) 
            else:
                form.add_error('group', "You don't have convention role for this group.")
                kwargs['group_form'] = form
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class PostCreationView(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    """
    Post creation view, it create with TemplateView so  i have to use additional form(PostCreationForm). 
    This form have inherited from forms.ModelForm
    View checks wheter you are in post_creators group or not before it sends form.
    """
    template_name = 'authorization/create.html'
    login_url = reverse_lazy('profile-login')

    def get(self, request, *args, **kwargs):
        form = PostCreationForm()
        del form.fields['author']
        kwargs['form'] = form
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # get information from request and create new data set
        values_dict = {}
        for key,value in request.POST.items():
            values_dict[key] = value
        values_dict['author'] = request.user.profile.creator
        form = PostCreationForm(values_dict)
        if form.is_valid():
            # add +1 the number of content
            self.request.user.profile.creator.number_of_content +=1
            self.request.user.profile.creator.save()
            form.save()
            return HttpResponseRedirect(reverse('authorization-main'))
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
        
    def test_func(self):
        return self.request.user.groups.filter(name__in = ['post_creators']).exists()
    

class ReviewCreationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Review creation with CreateView, You have to be in review_creators group to create any review.
    """
    model = Review
    fields = [
        'title', 'content', 'post'
    ]
    template_name = 'authorization/create.html'
    login_url = reverse_lazy('profile-login')
    success_url = reverse_lazy('authorization-main')

    def test_func(self):
        return self.request.user.groups.filter(name__in = ['review_creators']).exists()

    def form_valid(self, form):
        # add +1 to the number of the content 
        # set author to current creator that log in
        self.request.user.profile.creator.number_of_content +=1
        self.request.user.profile.creator.save()
        form.instance.author = self.request.user.profile.creator
        return super().form_valid(form)


class PostDetailView(DetailView):
    """
    view to show detail about post
    """
    model = Post
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'authorization/detail_post.html'
    context_object_name = 'post'


class PostUpdateMetaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View update the meta data(slug, status and puhlish date), Also check the user groups wheter it is meta_editors or not.
    """
    model = Post
    fields = [
        'slug', 'status', 'published_at'
    ]
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')

    def test_func(self):
        return self.request.user.groups.filter(name='meta_editors').exists()

    def form_valid(self, form):
        self.request.user.profile.editor.number_of_edited_content +=1
        self.request.user.profile.editor.save()
        return super().form_valid(form)


class PostUpdateContentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View update the content(title and content field), You have to be content editors(a group) or creator himself to update
    """
    model = Post
    fields = [
        'title', 'content'
    ]
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')

    def test_func(self):
        if self.request.user.groups.filter(name='content_editors').exists():
            return True
        elif hasattr(self.request.user.profile,'creator') :
            if self.get_object().author == self.request.user.profile.creator:
                return True
        return False
    
    def form_valid(self, form):
        if hasattr(self.request.user.profile, 'editor'):
            self.request.user.profile.editor.number_of_edited_content +=1
            self.request.user.profile.editor.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Basic delete view but also check the group before delete post permanently
    """
    model = Post
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')
    success_url = reverse_lazy('authorization-main')

    def test_func(self):
        return self.request.user.groups.filter(name='special_users').exists()


class ReviewDetailView(DetailView):
    """
    view to show detail about review
    """
    model = Review
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'authorization/detail_review.html'
    context_object_name = 'review'


class ReviewUpdateMetaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View update the meta data(slug, status and puhlish date), Also check the user groups wheter it is meta_editors or not.
    """
    model = Review
    fields = [
        'slug', 'status', 'published_at'
    ]
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')

    def test_func(self):
        return self.request.user.groups.filter(name='meta_editors').exists()

    def form_valid(self, form):
        self.request.user.profile.editor.number_of_edited_content +=1
        self.request.user.profile.editor.save()
        return super().form_valid(form)


class ReviewUpdateContentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View update the content(title and content field), You have to be content editors(a group) or creator himself to update
    """
    model = Review
    fields = [
        'title', 'content'
    ]
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')

    def test_func(self):
        if self.request.user.groups.filter(name='content_editors').exists():
            return True
        elif hasattr(self.request.user.profile,'creator') :
            if self.get_object().author == self.request.user.profile.creator:
                return True
        return False
    
    def form_valid(self, form):
        if hasattr(self.request.user.profile, 'editor'):
            self.request.user.profile.editor.number_of_edited_content +=1
            self.request.user.profile.editor.save()
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Basic delete view but also check the group before delete review permanently
    """
    model = Review
    template_name = 'authorization/update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    login_url = reverse_lazy('profile-login')
    success_url = reverse_lazy('authorization-main')

    def test_func(self):
        return self.request.user.groups.filter(name='special_users').exists()