from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class HelloTests(APITestCase):
    def setUp(self):
        User.objects.create_user("testuser", "testuser@mapros.be", "testpass")
        url = "/auth/"
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

    def test_hello(self):
        url = "/hello/"
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
