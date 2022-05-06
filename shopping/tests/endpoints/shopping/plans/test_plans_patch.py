from typing import OrderedDict

import pytest
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
    def test_if_anonymous_user_patching_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not edit a Plan.
        """

        plan = baker.make(Plan)

        data = {"name": "My Super Plan"}

        response = self.client.patch(endpoint(plan.id), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_put_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be patched to plans
        """

        plan = baker.make(Plan, user_id=1)

        data = {"name": ""}

        url = endpoint(plan.id)

        response = self.client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.

    def test_put_data_returns_valid_200_ok(self):
        """
        Ensure valid data cab be patched to plans
        """

        plan = baker.make(Plan, user_id=1)

        data = {"name": "My New Plan Name"}

        url = endpoint(plan.id)

        response = self.client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["name"] == data["name"]
