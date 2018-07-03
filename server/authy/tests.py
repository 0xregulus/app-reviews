from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()



class TestAuthAPI(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'insertstrongpassword'
        self.user = User.objects.create_user(
            self.username, 'user@test.com', self.password
        )
        self.client = APIClient()

    def test_login(self):
        url = reverse('authy')

        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('id'), self.user.id)
        self.assertEqual(response.json().get('username'), self.user.username)
        self.assertEqual(response.json().get('email'), self.user.email)
        self.assertEqual(response.json().get('is_staff'), self.user.is_staff)
