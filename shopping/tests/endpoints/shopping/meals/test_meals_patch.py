import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Ingredient, Meal, MealIngredient, Plan


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

    def test_patch_data_with_new_meal_ingredients_returns_valid_201_created(self):

        """
        Ensure we can add ingredients to an existing meal that already has an ingredient
        """

        meal = baker.make_recipe("shopping.meal_one")

        ingredient_one = baker.make_recipe("shopping.ingredient_one")
        ingredient_two = baker.make_recipe("shopping.ingredient_two")
        ingredient_three = baker.make_recipe("shopping.ingredient_three")

        baker.make(MealIngredient, meal=meal, ingredient=ingredient_one)

        data = {
            "meal_ingredients": [
                {"ingredient": ingredient_two.id, "quantity": 9999, "unit": "l"},
                {"ingredient": ingredient_three.id, "quantity": 9999, "unit": "g"},
            ],
        }

        url = endpoint(meal.id)

        response = self.client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["meal_ingredients"] != []
        assert len(response.data["meal_ingredients"]) == 3
