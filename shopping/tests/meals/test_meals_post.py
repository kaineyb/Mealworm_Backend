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
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create a Plan Days.
        """

        data = {"name": "My Lovely New Meal"}
        response = self.client.post(endpoint(), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted to Meals
        """

        data = {"name": ""}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        data = {"name": "My Lovely Meal"}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
