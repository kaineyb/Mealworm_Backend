import pytest
from core.models import User
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


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_deleting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not delete a Meal.
        """
        meal = baker.make_recipe("shopping.meal_one")

        response = self.client.delete(endpoint(meal.id), format="json")

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

    def test_delete_data_returns_204_no_content(self):

        meal = baker.make(Meal, user_id=self.user_id)

        url = endpoint(meal.id)

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_meal_deletes_meal_ingredient(self):

        meal = baker.make(Meal, user_id=self.user_id)
        ingredient = baker.make(Ingredient, user_id=self.user_id, name="My Ingredient")
        meal_ingredient = baker.make(MealIngredient, meal=meal, ingredient=ingredient)

        url = endpoint(meal.id)

        result = MealIngredient.objects.filter(pk=meal_ingredient.pk).first()
        assert result

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        result = MealIngredient.objects.filter(pk=meal_ingredient.pk).first()
        assert result == None
