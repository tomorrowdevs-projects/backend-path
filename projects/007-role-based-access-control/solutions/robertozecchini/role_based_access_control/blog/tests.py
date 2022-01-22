from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User

from .models import Post

class SimpleTests(TestCase):
    testuser_name = 'testuser'
    testuser_password = 'secret'
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=self.testuser_name,
            email='test@email.com',
            password=self.testuser_password
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)
    
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')
    
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')
    
    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)
    
    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
    
    def test_registered_view(self):
        response = self.client.get('/registered/')
        self.assertRedirects(response,'/accounts/login/?next=/registered/',status_code=302,target_status_code=200)
        self.client.login(username=self.testuser_name, password=self.testuser_password)
        response = self.client.get('/registered/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'only_registered.html')
        self.client.logout()
    
    def test_paying_view(self):
        response = self.client.get('/paying/')
        self.assertRedirects(response,'/accounts/login/?next=/paying/',status_code=302,target_status_code=200)
        self.client.login(username=self.testuser_name, password=self.testuser_password)
        response = self.client.get('/paying/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.client.logout()
        group, created = Group.objects.get_or_create(name = 'paying')
        self.user.groups.add(group)
        self.client.login(username=self.testuser_name, password=self.testuser_password)
        response = self.client.get('/paying/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'only_paying.html')
        self.client.logout()
        self.user.groups.clear()
