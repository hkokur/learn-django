from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from .models import Post
from .form import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


# Class-Based
class HomePage(TemplateView):
    template_name = "home.html"


class BlogPagination(ListView):
    model= Post
    context_object_name= "post_list"
    template_name= "blog/c/blog_pagination.html"
    paginate_by= 2
    queryset= Post.objects.order_by("-update")


class BlogCreate(CreateView):
    model = Post
    fields = ["title","status","content"]
    template_name = "blog/c/blog_create.html"

    def get_success_url(self):
        return reverse('class_detail', kwargs = { "slug" : self.object.slug })


class BlogDeatil(DetailView):
    model = Post
    template_name = "blog/c/blog_detail.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug == "get-random-post":
            obj = Post.objects.order_by("?")[0]
            return obj
        return super().get_object(queryset)


class BlogUpdate(UpdateView):
    model = Post
    fields = ['title', 'status', 'content']
    template_name = 'blog/c/blog_update.html'
    
    def get_success_url(self):
        return reverse('class_detail', kwargs = { "slug" : self.object.slug })
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug == "get-random-post":
            obj = Post.objects.order_by("?")[0]
            return obj
        return super().get_object(queryset)


class BlogDelete(DeleteView):
    model = Post
    template_name = "blog/c/blog_delete.html"
    success_url = reverse_lazy("class_pagination", args = [1])

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug == "get-random-post":
            obj = Post.objects.order_by("?")[0]
            return obj
        return super().get_object(queryset)


# Function-Based
def blog_main(request):
    return render(request, "blog/blog.html")


def blog_pagination(request,page):
    all_post = Post.objects.all().order_by("-update")
    paginator = Paginator(all_post,2)
    post_list = paginator.get_page(page)
    context = {
        "post_list" : post_list
    }
    return render(request,"blog/f/blog_pagination.html",context=context)


def blog_create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            obj = post_form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect("func_detail", slug=obj.slug)
    post_form = PostForm()
    context = {
        "form" : post_form
    }
    return render(request,"blog/f/blog_create.html",context)


def blog_detail(request, slug):
    if slug == "get-random-post":
        post = Post.objects.order_by("?")[0]
    else:
        post = get_object_or_404(Post, slug=slug)
    context = {
        "post" : post
    }
    return render(request, "blog/f/blog_detail.html", context)


def blog_update(request, slug):
    if slug == "get-random-post":
        obj = Post.objects.order_by("?")[0]
    else:
        obj = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=obj)
        if post_form.is_valid():
            obj = post_form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect("func_detail", slug=slug)
    post_form = PostForm(instance=obj)
    context = {
        "form" : post_form
    }
    return render(request, "blog/f/blog_update.html", context)
    

def blog_delete(request, slug):
    if slug == "get-random-post":
        obj = Post.objects.order_by("?")[0]
    else:
        obj = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        obj.delete()
        return redirect("func_pagination", page=1)
    context = {
        "post" : obj
    }
    return render(request, "blog/f/blog_delete.html", context)
