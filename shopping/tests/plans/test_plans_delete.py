from typing import OrderedDict
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from shopping.models import Plan, Day
from model_bakery import baker


from pprint import pprint


def endpoint(plan_id=None):
    list = f"/shopping/plans/"
    detail = list + f"{plan_id}/"

    if plan_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_deleting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not delete a Plan.
        """

        plan = baker.make(Plan)

        response = self.client.delete(endpoint(plan.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        url = "/auth/users/"

        data = {
            "email": "test@test.com",
            "username": "TestUser",
            "password": "TestPassword",
        }

        self.client.post(url, data, format="json")

        self.user["id"] = User.objects.get().id
        self.user["email"] = User.objects.get().email
        self.user["username"] = User.objects.get().username

        print(f"SetUp User ID is: {self.user['id']}")

        user = User.objects.get(pk=self.user["id"])
        self.client.force_authenticate(user=user)

    def test_delete_data_returns_204_no_content(self):

        plan = baker.make(Plan, user_id=1, name="Awesome Plan", start_day="Tues")

        url = endpoint(plan.id)

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
