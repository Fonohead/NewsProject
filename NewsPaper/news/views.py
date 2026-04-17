from django.views.generic import ListView, DetailView
from .models import Post
from django.shortcuts import render

def home(request):
    return render(request, 'flatpages/main.html')

class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'

