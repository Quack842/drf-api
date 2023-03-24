from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTest(APITestCase):
    def setUp(self):
        # Have to use an existing acc. so using adam instead
        User.objects.create_user(username='Admin', password='pass')

    def test_can_list_posts(self):
        admin = User.objects.get(username='Admin')
        Post.objects.create(owner=admin, title='a title')
        responce = self.client.get('/posts/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='Admin', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
