from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from shopping.models import Plan
from model_bakery import baker


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

    def test_if_anonymous_user_getting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not get any stores.
        """
        baker.make(Plan)

        response = self.client.get(endpoint())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


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

    def test_get_data_returns_valid_200_ok(self):

        plan = baker.make(Plan, user_id=1)

        url = endpoint(plan.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["name"] == plan.name
        assert response.data["start_day"] == plan.start_day

    def test_patch_data_returns_valid_200_ok(self):

        # Create a Section/Aisle so we can test:
        plan = baker.make(Plan, user_id=1, name="Awesome Plan", start_day="Tues")

        url = endpoint(plan.id)

        data = {"name": "Test Plan 2", "start_day": "Wed"}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["start_day"] == data["start_day"]

    def test_delete_data_returns_204_no_content(self):

        plan = baker.make(Plan, user_id=1, name="Awesome Plan", start_day="Tues")

        url = endpoint(plan.id)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
