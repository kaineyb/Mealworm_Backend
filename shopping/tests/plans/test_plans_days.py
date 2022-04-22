import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from shopping.models import Plan, Day, Meal

from setup import create_user

from model_bakery import baker
import json


def endpoint(plan_id=1, days_id=None):
    days_list = f"/shopping/plans/{plan_id}/days/"
    days_detail = days_list + f"{days_id}/"

    if days_id:
        return days_detail
    else:
        return days_list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create a Plan Days.
        """

        data = {"order": 1, "meal": 1}
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

        self.plan = baker.make(Plan, user_id=self.user_id)
        self.meal = baker.make(Meal, user_id=self.user_id)

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted to Plan Days
        """

        data = {"order": -1, "meal": ""}
        url = endpoint(self.plan.id)

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["meal"] is not None
        )  # Checks that we get an validation error.
        assert (
            response.data["order"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        data = {"order": 1, "meal": self.meal.id}
        url = endpoint(self.plan.id)

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["order"] == data["order"]
        assert response.data["meal"] == data["order"]

    def test_get_data_returns_valid_200_ok(self):

        day = baker.make(Day, meal_id=self.meal.id, plan_id=self.plan.id)

        url = endpoint(self.plan.id, day.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["order"] == day.order

        assert response.data["meal"]["id"] == self.meal.id
        assert response.data["meal"]["name"] == self.meal.name

    def test_patch_data_returns_valid_200_ok(self):

        # Create a Section/Aisle so we can test:
        day = baker.make(Day, meal_id=self.meal.id, plan_id=self.plan.id)

        url = endpoint(self.plan.id, day.id)

        data = {"order": 999, "meal": self.meal.id}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["order"] == data["order"]
        assert response.data["meal"] == data["meal"]

    def test_delete_data_returns_204_no_content(self):

        day = baker.make(Day, meal_id=self.meal.id, plan_id=self.plan.id)

        url = endpoint(self.plan.id, day.id)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
