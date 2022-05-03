from typing import OrderedDict

import pytest
from core.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Day, Plan


def endpoint(plan_id=None):
    list = f"/shopping/plans/"
    detail = list + f"{plan_id}/"

    if plan_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_puting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not edit a Plan.
        """

        plan = baker.make(Plan)

        data = {"name": "My Super Plan", "start_day": "Tues"}

        response = self.client.put(endpoint(plan.id), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_put_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be put to plans
        """

        plan = baker.make(Plan, user_id=1)

        data = {"name": "", "start_day": 1}

        url = endpoint(plan.id)

        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.

        assert (
            response.data["start_day"] is not None
        )  # Checks that we get an validation error.

    def test_put_data_returns_valid_200_ok(self):
        """
        Ensure valid data can be put
        """

        plan = baker.make(Plan, user_id=1)

        data = {"name": "My Awesome Plan", "start_day": "Tue"}
        url = endpoint(plan.id)

        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]

    def test_put_data_with_day_set_blank_returns_valid_200_ok(self):
        """
        Ensure valid data can be posted with a blank day_set
        """

        plan = baker.make(Plan, user_id=1)
        url = endpoint(plan.id)

        data = {"name": "My Awesome Plan", "start_day": "Tue", "day_set": []}

        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]
        assert response.data["day_set"] == data["day_set"]

    def test_put_data_with_day_set_correct_returns_valid_200_ok(self):
        """
        Ensure valid data can be posted with a correct day_set
        """

        plan = baker.make_recipe("shopping.plan_one")
        url = endpoint(plan.id)

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

        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
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

    def test_put_data_with_day_already_created_returns_valid_200_ok(
        self,
    ):
        """
        Ensure valid data can be posted with a correct day_set and a day already created
        """

        plan = baker.make_recipe("shopping.plan_one")
        url = endpoint(plan.id)

        # Arrange
        meal_one = baker.make_recipe("shopping.meal_one")
        meal_two = baker.make_recipe("shopping.meal_two")
        meal_three = baker.make_recipe("shopping.meal_three")

        day_one = baker.make(Day, meal=meal_one, plan=plan)

        days = [
            {"id": day_one.id, "order": 1, "meal": meal_one.id},
            {"order": 2, "meal": meal_two.id},
            {"order": 3, "meal": meal_three.id},
        ]

        data = {"name": "My Awesome Plan", "start_day": "Tue", "day_set": days}

        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
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

    def test_put_new_days_deletes_unused_days_returns_valid_200_ok(self):
        """
        Ensure when we update the days, the other days are deleted, should work from the models.
        """

        plan = baker.make_recipe("shopping.plan_one")
        url = endpoint(plan.id)

        # Arrange
        meal_one = baker.make_recipe("shopping.meal_one")
        meal_two = baker.make_recipe("shopping.meal_two")

        day_one = baker.make(Day, meal=meal_one, plan=plan, order=1)
        day_two = baker.make(Day, meal=meal_one, plan=plan, order=2)
        day_three = baker.make(Day, meal=meal_one, plan=plan, order=3)

        days = [
            {"order": 4, "meal": meal_two.id},
            {"order": 5, "meal": meal_two.id},
            {"order": 6, "meal": meal_two.id},
        ]

        data = {"name": "My Awesome Plan", "start_day": "Tue", "day_set": days}

        response = self.client.put(url, data, format="json")
        print("response.data", response.data)

        assert response.status_code == status.HTTP_200_OK

        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]
        assert response.data["day_set"] != []

        assert response.data["day_set"] == [
            OrderedDict(
                [
                    ("id", days[0]["order"]),
                    ("order", days[0]["order"]),
                    ("meal", days[0]["meal"]),
                ]
            ),
            OrderedDict(
                [
                    ("id", days[1]["order"]),
                    ("order", days[1]["order"]),
                    ("meal", days[1]["meal"]),
                ]
            ),
            OrderedDict(
                [
                    ("id", days[2]["order"]),
                    ("order", days[2]["order"]),
                    ("meal", days[2]["meal"]),
                ]
            ),
        ]
