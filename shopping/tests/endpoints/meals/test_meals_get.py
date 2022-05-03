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


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_getting_returns_401_unauthorised(self):
        """
        Ensure an anonymous user can not get any Plan Days.
        """

        response = self.client.get(endpoint())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_get_data_returns_valid_200_ok(self):

        meal = baker.make(Meal, user_id=self.user_id)

        url = endpoint(meal.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["name"] == meal.name

    def test_get_wrong_id_return_invalid_404_not_found(self):

        url = endpoint(1)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
