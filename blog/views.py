from django.views.generic import TemplateView, ListView
from .models import Post
from django.shortcuts import render
from django.core.paginator import Paginator

class HomePage(TemplateView):
    template_name = "blog/home.html"

def blog_main(request):
    return render(request, "blog/blog.html")

def blog_pagination(request,page):
    all_post = Post.objects.all().filter(status="pu")
    paginator = Paginator(all_post,2)
    post_list = paginator.get_page(page)

    context = {
        "post_list" : post_list
    }

    return render(request,"blog/blog_func.html",context=context)


class BlogPagination(ListView):
    model= Post
    context_object_name= "post_list"
    template_name= "blog/blog_class.html"
    paginate_by= 2
    queryset= Post.objects.filter(status="pu")
