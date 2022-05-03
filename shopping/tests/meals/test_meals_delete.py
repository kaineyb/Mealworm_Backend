import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from shopping.models import Plan, Day, Meal
from core.models import User

from setup import create_user

from model_bakery import baker


def endpoint(meal_id=None):
    list = f"/shopping/meals/"
    detail = list + f"{meal_id}/"

    if meal_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_deleting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not delete a Meal.
        """
        user = baker.make(User)
        meal = baker.make_recipe("shopping.meal_one")

        response = self.client.delete(endpoint(meal.id), format="json")

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

        meal = baker.make(Meal, user_id=self.user_id)

        url = endpoint(meal.id)

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
