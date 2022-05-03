from typing import OrderedDict
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from shopping.models import Plan, Day
from model_bakery import baker


def endpoint(plan_id=None):
    list = f"/shopping/plans/"
    detail = list + f"{plan_id}/"

    if plan_id:
        return detail
    else:
        return list


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_getting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not get any stores.
        """
        plan = baker.make(Plan)

        response = self.client.get(endpoint())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response_id = self.client.get(endpoint(plan.id))
        assert response_id.status_code == status.HTTP_401_UNAUTHORIZED


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

        print(f"SetUp User ID is: {self.user['id']}")

        user = User.objects.get(pk=self.user["id"])
        self.client.force_authenticate(user=user)

    def test_get_data_returns_valid_200_ok(self):

        plan = baker.make(Plan, user_id=1)

        url = endpoint(plan.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["name"] == plan.name
        assert response.data["start_day"] == plan.start_day

    def test_get_full_data_returns_valid_200_ok(self):

        # Arrange
        plan = baker.make_recipe("shopping.plan_one")

        meal_one = baker.make_recipe("shopping.meal_one")
        meal_two = baker.make_recipe("shopping.meal_two")
        meal_three = baker.make_recipe("shopping.meal_three")

        day_one = baker.make(Day, order=1, meal_id=meal_one.id, plan_id=plan.id)
        day_two = baker.make(Day, order=2, meal_id=meal_two.id, plan_id=plan.id)
        day_three = baker.make(Day, order=3, meal_id=meal_three.id, plan_id=plan.id)

        # Act
        url = endpoint(plan.id)
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["name"] == plan.name
        assert response.data["start_day"] == plan.start_day

        assert response.data["day_set"] == [
            OrderedDict(
                [
                    ("id", day_one.id),
                    ("order", day_one.order),
                    ("meal", day_one.meal_id),
                ]
            ),
            OrderedDict(
                [
                    ("id", day_two.id),
                    ("order", day_two.order),
                    ("meal", day_two.meal_id),
                ]
            ),
            OrderedDict(
                [
                    ("id", day_three.id),
                    ("order", day_three.order),
                    ("meal", day_three.meal_id),
                ]
            ),
        ]

    def test_get_day_set_has_both_day_and_meal_id(self):
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
        day_set = OrderedDict()
        day_set["id"] = day.id
        day_set["order"] = day.order
        day_set["meal"] = meal.id

        # Act
        response = self.client.get(url)

        # Assert

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == plan.id
        assert response.data["name"] == plan.name
        assert response.data["start_day"] == plan.start_day
        assert response.data["day_set"] == [day_set]
