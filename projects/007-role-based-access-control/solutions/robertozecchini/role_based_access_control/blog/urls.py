# blog/urls.py

from django.urls import path
from .views import AboutPageView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, RegisteredPageView, PayingPageView

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('registered/', RegisteredPageView.as_view(), name='registered'),
    path('paying/', PayingPageView.as_view(), name='paying'),
    path('about/', AboutPageView.as_view(), name='about'),
]