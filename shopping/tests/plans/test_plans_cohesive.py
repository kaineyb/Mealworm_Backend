import pytest
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User

from shopping.models import Plan, Day, Meal
from model_bakery import baker

from collections import OrderedDict


def endpoint(plan_id=None):
    list = f"/shopping/plans/"
    detail = list + f"{plan_id}/"

    if plan_id:
        return detail
    else:
        return list


class TestAuthUser(APITestCase):

    user = {}

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        url = "/auth/users/"

        data = {
            "email": "test@test.com",
            "username": "TestUser",
            "password": "TestPassword",
        }

        self.client.post(url, data, format="json")

        self.user["id"] = User.objects.get().id
        self.user["email"] = User.objects.get().email
        self.user["username"] = User.objects.get().username

        # print(f"SetUp User ID is: {self.user['id']}")

        user = User.objects.get(pk=self.user["id"])
        self.client.force_authenticate(user=user)

    def test_plan_days_have_both_day_and_meal_id(self):
        """
        Checks that we have both a Plan ID and a Day ID
        """

        # Arrange

        plan = baker.make_recipe("shopping.plan_one")
        meal = baker.make_recipe("shopping.meal_one")
        day = baker.make(Day, plan_id=plan.id, meal_id=meal.id, order=1)

        url = endpoint(plan.id)

        # We want to see a dictionary like the below:
        # {"id": 1, "order": 1, "meal":  meal.id}
        plan_days = OrderedDict()
        plan_days["id"] = day.id
        plan_days["order"] = day.order
        plan_days["meal"] = meal.id

        # Act
        response = self.client.get(url)

        # Assert

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == plan.id
        assert response.data["name"] == plan.name
        assert response.data["start_day"] == plan.start_day
        assert response.data["plan_days"] == [plan_days]
