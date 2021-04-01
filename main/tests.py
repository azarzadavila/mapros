from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

username = "testuser"
password = "testpass"
url_theorem_statements = "/theorem_statements/"


class AuthentificationTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username=username, password=password)

    def test_get_token(self):
        data = {"username": username, "password": password}
        response = self.client.post(url_auth, data, format="json")
        user = User.objects.get(username=username)
        token = Token.objects.get(user=user)
        token = token.key
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], token)
        self.assertDictEqual(
            response.data["user"], {"id": user.id, "username": user.username}
        )

    def test_wrong_credentials(self):
        def __incorrect(data):
            response = self.client.post(url_auth, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        __incorrect({"username": "i", "password": password})
        __incorrect({"username": username, "password": "i"})

    def test_incorrect(self):
        def __incorrect(data):
            response = self.client.post(url_auth, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        __incorrect({})
        __incorrect({"username": "a"})
        __incorrect({"password": "a"})

