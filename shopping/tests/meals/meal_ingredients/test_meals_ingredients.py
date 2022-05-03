import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from shopping.models import Ingredient, MealIngredient, Plan, Day, Meal
from core.models import User

from setup import create_user

from model_bakery import baker


def endpoint(meal_id=1, meal_ingredient_id=None) -> str:
    list = f"/shopping/meals/{meal_id}/ingredients/"
    detail = list + f"{meal_ingredient_id}/"

    if meal_ingredient_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not add an ingredient to a meal.
        """
        user = baker.make(User)
        meal = baker.make(Meal)
        ingredient = baker.make(Ingredient, user_id=user.id)

        url = endpoint(meal.id)

        data = {"ingredient": ingredient.id, "quantity": 1000, "unit": "g"}
        response = self.client.post(url, data, format="json")

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

        self.ingredient = baker.make(Ingredient, user_id=self.user_id)
        self.meal = baker.make(Meal, user_id=self.user_id)

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted to meal/<int:pk>/ingredients
        """

        data = {"ingredient": 0, "quantity": "", "unit": ""}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["ingredient"] is not None
        )  # Checks that we get an validation error.
        assert (
            response.data["quantity"] is not None
        )  # Checks that we get an validation error.
        assert (
            response.data["unit"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        data = {"ingredient": self.ingredient.id, "quantity": 1000, "unit": "g"}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["ingredient"] == data["ingredient"]
        assert response.data["quantity"] == data["quantity"]
        assert response.data["unit"] == data["unit"]

    def test_get_data_returns_valid_200_ok(self):

        meal_ingredient = baker.make(
            MealIngredient, meal_id=self.meal.id, ingredient_id=self.ingredient.id
        )

        url = endpoint(self.meal.id, meal_ingredient.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["ingredient"] == self.ingredient.id

        assert response.data["quantity"] == meal_ingredient.quantity
        assert response.data["unit"] == meal_ingredient.unit

    def test_patch_data_returns_valid_200_ok(self):

        meal_ingredient = baker.make(
            MealIngredient, meal_id=self.meal.id, ingredient_id=self.ingredient.id
        )

        url = endpoint(self.meal.id, meal_ingredient.id)

        data = {"quantity": 1000, "unit": "ml"}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["quantity"] == data["quantity"]
        assert response.data["unit"] == data["unit"]

    def test_delete_data_returns_204_no_content(self):

        meal_ingredient = baker.make(
            MealIngredient, meal_id=self.meal.id, ingredient_id=self.ingredient.id
        )

        url = endpoint(self.meal.id, meal_ingredient.id)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
