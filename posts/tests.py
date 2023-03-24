from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.response import Response


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


class PostDetailViewTests(APITestCase):
    def setUp(self):
        admin = User.objects.create_user(username='Admin', password='pass')
        admin2 = User.objects.create_user(username='Admin2', password='pass')
        Post.objects.create(
            owner=admin, title='This is title', content='Admin content'
        )
        Post.objects.create(
            owner=admin2, title='another title', content='Admin2 content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['title'], 'This is title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='Admin', password='pass')
        response = self.client.put('/posts/1', {'title': 'This is new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'This is new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='admin', password='pass')
        response = self.client.put('/posts/2', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
