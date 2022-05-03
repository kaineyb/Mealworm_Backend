from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User

from setup import create_user


class TestCreateUser(APITestCase):

    test_user = {}

    def setUp(self):
        """Create a Test User"""
        create_user(self, self.test_user)

    def test_create_user_returns_201_created(self):
        """
        Ensure we can create a new account object.
        """
        url = "/auth/users/"

        data = {
            "email": "test2@test.com",
            "username": "TestUser2",
            "password": "TestPassword2",
        }

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() > 0
        assert (
            User.objects.filter(username=data["username"]).get().username
            == data["username"]
        )


class TestAnonUserInfo(APITestCase):
    def test_if_user_anonymous_returns_401_unauthorized(self):
        """
        Ensure anonymous user cannot see user info
        """
        url = "/auth/users/"

        response = self.client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
