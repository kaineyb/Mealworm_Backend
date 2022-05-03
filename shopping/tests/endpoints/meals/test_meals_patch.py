import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Meal, MealIngredient, Plan


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

    @pytest.mark.skip
    def test_patch_data_with_meal_ingredients_returns_valid_200_ok(self):

        """When patched with empty meal_ingredient, should remove all meal ingredients"""

        meal = baker.make(Meal, user_id=self.user_id)
        meal_ingredient = baker.make(MealIngredient, meal=meal)

        url = endpoint(meal.id)

        data = {"name": "My New Meal Name", "meal_ingredients": []}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meal_ingredients"] == []
