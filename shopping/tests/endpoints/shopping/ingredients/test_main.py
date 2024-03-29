import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from shopping.models import Ingredient, Plan, Day, Meal, Section

from setup import create_user

from model_bakery import baker


def endpoint(ingredient_id=None):
    list = f"/shopping/ingredients/"
    detail = list + f"{ingredient_id}/"

    if ingredient_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create a Plan Days.
        """

        data = {"name": "", "section": 0}
        response = self.client.post(endpoint(), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted to Meals
        """

        data = {"name": "", "section": 0}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.
        assert (
            response.data["section"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        section = baker.make(Section, user_id=self.user_id)

        data = {"name": "Red Pepper", "section": section.id}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_get_data_returns_valid_200_ok(self):

        ingredient = baker.make(Ingredient, user_id=self.user_id)

        url = endpoint(ingredient.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["name"] == ingredient.name

    def test_patch_data_returns_valid_200_ok(self):

        ingredient = baker.make(Ingredient, user_id=self.user_id)

        url = endpoint(ingredient.id)

        data = {"name": "My New Meal Name"}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]

    def test_delete_data_returns_204_no_content(self):

        ingredient = baker.make(Ingredient, user_id=self.user_id)

        url = endpoint(ingredient.id)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
