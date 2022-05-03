from core.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Store


class TestAnon(APITestCase):
    endpoint = "/shopping/stores/"

    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create a store.
        """

        data = {"name": "Test Store"}

        response = self.client.post(self.endpoint, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_anonymous_user_getting_returns_401_unauthorised(self):
        """
        Ensure an anonymous user can not get any stores.
        """

        response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuth(APITestCase):

    user = {}
    endpoint = "/shopping/stores/"

    def setUp(self):
        """
        Create a User and Authenticate for Testing
        """
        create_user(self, self.user)

        self.user_id = self.user["id"]

    def test_post_data_returns_invalid_400_bad_request(self):
        """
        Ensure invalid data cannot be posted
        """

        data = {"name": ""}

        response = self.client.post(self.endpoint, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["name"] is not None
        )  # Checks that we get an validation error.

    def test_post_data__returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """
        data = {"name": "test"}

        response = self.client.post(self.endpoint, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["name"] == data["name"]

    def test_get_data_returns_valid_200_ok(self):

        store = baker.make(Store, user_id=1)

        response = self.client.get(f"{self.endpoint}{store.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_patch_data_returns_valid_200_ok(self):

        store = baker.make(Store, user_id=1)

        data = {"name": "New Name"}

        response = self.client.patch(f"{self.endpoint}{store.id}/", data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]

    def test_delete_data_returns_204_no_content(self):

        store = baker.make(Store, user_id=1)

        response = self.client.get(f"{self.endpoint}{store.id}/")
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(f"{self.endpoint}{store.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
