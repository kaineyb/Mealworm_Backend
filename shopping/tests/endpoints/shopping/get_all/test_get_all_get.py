import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping import models

ENDPOINT = f"/shopping/get_all/"


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_getting_returns_401_unauthorised(self):
        """
        Ensure an anonymous user can not get any Plan Days.
        """

        response = self.client.get(ENDPOINT)

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

    def test_get_data_returns_valid_200_ok(self):

        response = self.client.get(ENDPOINT)

        assert response.status_code == status.HTTP_200_OK

    def test_get_data_returns_valid_200_ok_with_empty_lists(self):

        response = self.client.get(ENDPOINT)

        assert response.data == {
            "stores": [],
            "sections": [],
            "plans": [],
            "ingredients": [],
            "meals": [],
        }

    def test_get_data_with_actual_data_returns_valid_200_ok(self):

        baker.make(models.Store, user_id=self.user_id)
        baker.make(models.Section, user_id=self.user_id)

        baker.make(models.Plan, user_id=self.user_id)
        baker.make(models.Ingredient, user_id=self.user_id)
        baker.make(models.Meal, user_id=self.user_id)

        response = self.client.get(ENDPOINT)

        assert response.data["stores"] != []
        assert response.data["sections"] != []
        assert response.data["plans"] != []
        assert response.data["ingredients"] != []
        assert response.data["meals"] != []
