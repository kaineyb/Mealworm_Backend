from typing import OrderedDict

from core.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Plan


def endpoint(plan_id=None):
    list = f"/shopping/plans/"
    detail = list + f"{plan_id}/"

    if plan_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create a Plan.
        """

        baker.make(Plan)

        data = {"name": "My Super Plan", "start_day": "Tues"}
        response = self.client.post(endpoint(), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):
    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted to plans
        """

        data = {"name": "", "start_day": 1}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.

        assert (
            response.data["start_day"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        data = {"name": "My Awesome Plan", "start_day": "Tue"}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]

    def test_post_data_with_day_set_blank_returns_valid_201_created(self):
        """
        Ensure valid data can be posted with a blank day_set
        """

        data = {"name": "My Awesome Plan", "start_day": "Tue", "day_set": []}
        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]
        assert response.data["day_set"] == data["day_set"]

    def test_post_data_with_day_set_correct_returns_valid_201_created(self):
        """
        Ensure valid data can be posted with a correct day_set
        """

        # Arrange
        meal_one = baker.make_recipe("shopping.meal_one")
        meal_two = baker.make_recipe("shopping.meal_two")
        meal_three = baker.make_recipe("shopping.meal_three")

        days = [
            {"order": 1, "meal": meal_one.id},
            {"order": 2, "meal": meal_two.id},
            {"order": 3, "meal": meal_three.id},
        ]

        data = {"name": "My Awesome Plan", "start_day": "Tue", "day_set": days}

        url = endpoint()

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]
        assert response.data["day_set"] != []

        assert response.data["day_set"] == [
            OrderedDict(
                [("id", 1), ("order", days[0]["order"]), ("meal", days[0]["meal"])]
            ),
            OrderedDict(
                [("id", 2), ("order", days[1]["order"]), ("meal", days[1]["meal"])]
            ),
            OrderedDict(
                [("id", 3), ("order", days[2]["order"]), ("meal", days[2]["meal"])]
            ),
        ]
