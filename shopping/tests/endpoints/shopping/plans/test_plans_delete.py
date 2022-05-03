from pprint import pprint
from typing import OrderedDict

from core.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Plan


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
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_delete_data_returns_204_no_content(self):

        plan = baker.make(Plan, user_id=1, name="Awesome Plan", start_day="Tues")

        url = endpoint(plan.id)

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
