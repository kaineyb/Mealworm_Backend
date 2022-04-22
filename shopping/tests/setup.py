from core.models import User
from rest_framework.test import APITestCase


def create_user(self: APITestCase, user: dict):
    """
    Used within SetUp, takes self, and a dictionary for output reference
    """

    url = "/auth/users/"

    data = {
        "email": "test@test.com",
        "username": "TestUser",
        "password": "TestPassword",
    }

    self.client.post(url, data, format="json")

    user["id"] = User.objects.get().id
    user["email"] = User.objects.get().email
    user["username"] = User.objects.get().username

    print(f"SetUp User ID is: {user['id']}")

    new_user = User.objects.get(pk=user["id"])
    self.client.force_authenticate(user=new_user)
