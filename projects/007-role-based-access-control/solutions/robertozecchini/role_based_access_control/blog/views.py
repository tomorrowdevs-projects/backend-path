from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post

class AboutPageView(TemplateView):
    template_name = 'about.html'

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'