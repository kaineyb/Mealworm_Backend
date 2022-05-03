from pprint import pprint

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

    def test_post_data_with_meal_ingredients_returns_valid_201_created(self):
        """
        Ensure valid data can be posted

        """

        ingredients = baker.make(Ingredient, _quantity=3)

        i = [x.id for x in ingredients]

        print(i)
        print(ingredients)

        new_shit = [
            {"id": 1, "ingredient": {"name": "Mince"}, "quantity": 500, "unit": "g"},
            {
                "id": 2,
                "ingredient": {"name": "Spaghetti Bolognese Sauce"},
                "quantity": 500,
                "unit": "ml",
            },
            {
                "id": 3,
                "ingredient": {"name": "Spaghetti"},
                "quantity": 500,
                "unit": "g",
            },
        ]

        data = {"name": "My Lovely Meal", "meal_ingredients": []}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
        # assert False
