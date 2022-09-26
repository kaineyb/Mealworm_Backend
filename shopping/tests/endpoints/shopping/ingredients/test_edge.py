import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Ingredient, Meal, Plan, Section


def endpoint(ingredient_id=None):
    list = f"/shopping/ingredients/"
    detail = list + f"{ingredient_id}/"

    if ingredient_id:
        return detail
    else:
        return list


class TestAuthUser(APITestCase):

    user = {}

    @pytest.mark.django_db
    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_create_ingredient_without_section_valid_201_created(self):
        """
        Ensure ingredient can be created without a section
        """

        data = {"name": "Red Pepper"}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
