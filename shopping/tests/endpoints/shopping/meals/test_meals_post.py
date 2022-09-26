import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Meal, Plan


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

    @pytest.mark.django_db
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

    def test_post_data_with_blank_meal_ingredients_returns_valid_201_created(self):
        """
        Ensure valid data can be posted with a blank meal_ingredients
        """

        data = {"name": "My Lovely Meal", "meal_ingredients": []}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_post_data_with_new_meal_ingredients_returns_valid_201_created(self):

        """
        Ensure we can create meal ingredients when we create a meal.
        We do first need the ingredient :)
        """

        ingredient_one = baker.make_recipe(
            "shopping.ingredient_one", user_id=self.user_id
        )
        ingredient_two = baker.make_recipe(
            "shopping.ingredient_two", user_id=self.user_id
        )
        ingredient_three = baker.make_recipe(
            "shopping.ingredient_three", user_id=self.user_id
        )

        data = {
            "name": "My New Meal",
            "meal_ingredients": [
                {"ingredient": ingredient_one.id, "quantity": 125, "unit": "ml"},
                {"ingredient": ingredient_two.id, "quantity": 250, "unit": "l"},
                {"ingredient": ingredient_three.id, "quantity": 500, "unit": "g"},
            ],
        }

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

        assert response.data["meal_ingredients"] != []

        assert response.data["meal_ingredients"][0]["id"] > 0
        assert response.data["meal_ingredients"][1]["id"] > 0
        assert response.data["meal_ingredients"][2]["id"] > 0
