import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from shopping.models import Plan, Day, Meal

from setup import create_user

from model_bakery import baker


def endpoint(meal_id=None):
    list = f"/shopping/meals/"
    detail = list + f"{meal_id}/"

    if meal_id:
        return detail
    else:
        return list


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_patch_data_returns_valid_200_ok(self):

        meal = baker.make(Meal, user_id=self.user_id)

        url = endpoint(meal.id)

        data = {"name": "My New Meal Name"}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
