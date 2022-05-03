import pytest
from core.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from setup import create_user
from shopping.models import Section, Store, StoreAisle


def endpoint(section_id: int, aisle_id: int = None):
    list = f"/shopping/sections/{section_id}/aisles/"
    detail = list + f"{aisle_id}/"

    if not aisle_id:
        return list
    else:
        return detail


class TestAnonUser(APITestCase):
    def test_if_anonymous_user_posting_returns_401_unauthorized(self):
        """
        Ensure an anonymous user can not create an Aisle.
        """

        section = baker.make(Section)

        data = {"store": 1, "aisle_number": 10}

        response = self.client.post(endpoint(section.id), data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_anonymous_user_getting_returns_401_unauthorised(self):
        """
        Ensure an anonymous user can not get any stores.
        """
        section = baker.make(Section)
        response = self.client.get(endpoint(section.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthUser(APITestCase):

    user = {}

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

        section = baker.make(Section, user_id=1)

        data = {"store": "", "aisle_number": ""}
        url = endpoint(section.id)

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["store"] is not None
        )  # Checks that we get an validation error.

    def test_post_data_returns_valid_201_created(self):
        """
        Ensure valid data can be posted
        """

        section = baker.make(Section, user_id=1)
        store = baker.make(Store, user_id=1)

        data = {"store": store.id, "aisle_number": 10}
        url = endpoint(section.id)

        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["store"] == data["store"]
        assert response.data["aisle_number"] == data["aisle_number"]

    def test_get_data_returns_valid_200_ok(self):

        # Create a Section/Aisle so we can test:
        section = baker.make(Section, user_id=1)
        store = baker.make(Store, user_id=1)
        store_aisle = baker.make(StoreAisle, store_id=store.id, section_id=section.id)

        url = endpoint(section.id, store_aisle.id)

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0
        assert response.data["store"] == store.id
        assert response.data["aisle_number"] == store_aisle.aisle_number

    def test_patch_data_returns_valid_200_ok(self):

        # Create a Section/Aisle so we can test:
        section = baker.make(Section, user_id=1)
        store = baker.make(Store, user_id=1)
        store_aisle = baker.make(StoreAisle, store_id=store.id, section_id=section.id)

        url = endpoint(section.id, store_aisle.id)

        data = {"store": store.id, "aisle_number": 10}

        response = self.client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["store"] == data["store"]
        assert response.data["aisle_number"] == data["aisle_number"]

    def test_delete_data_returns_204_no_content(self):

        # Create a Section/Aisle so we can test:
        section = baker.make(Section, user_id=1)
        store = baker.make(Store, user_id=1)
        store_aisle = baker.make(StoreAisle, store_id=store.id, section_id=section.id)

        url = endpoint(section.id, store_aisle.id)

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
