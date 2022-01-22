from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from .models import Post
import django.http as ht

def must_be_paying(user):
    return user.groups.filter(name='paying').count()

class PayingUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.user_type == 'paying'
        except:
            return False

class AboutPageView(TemplateView):
    template_name = 'about.html'

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

class RegisteredPageView(LoginRequiredMixin, TemplateView):
    template_name = 'only_registered.html'

class PayingPageView(PayingUserMixin, TemplateView):
    template_name = 'only_paying.html'