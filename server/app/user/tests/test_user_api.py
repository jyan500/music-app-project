"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
	User, 
	Friendship
)

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")

def create_user(**params):
	"""Create and return a new user."""
	return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
	"""Test the public features of the user API."""
	def setUp(self):
		self.client = APIClient()

	def test_create_user_success(self):
		"""Test creating a user is successful"""
		payload = {
			"email" : "test@example.com",	
			"password": "testpass123",
			"first_name": "Test",
			"last_name": "Name"
		}
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(email=payload["email"])
		self.assertTrue(user.check_password(payload["password"]))
		# make sure that the password is not part of the response data
		self.assertNotIn("password", res.data)

	# def test_create_user_with_friends(self):
	# 	"""Test creating a user is successful"""
	# 	friend1 = create_user(email="friend1@example.com", name="Test User 1", password="goodpass1")
	# 	friend2 = create_user(email="friend2@example.com", name="Test User 2", password="goodpass2")
	# 	payload = {
	# 		"email" : "test2@example.com",	
	# 		"password": "testpass123",
	# 		"name": "Test Name",
	# 		"friends": [{"friend": friend1.id}, {"friend": friend2.id}]
	# 	}
	# 	res = self.client.post(CREATE_USER_URL, payload, format="json")

	# 	self.assertEqual(res.status_code, status.HTTP_201_CREATED)
	# 	user = get_user_model().objects.get(email=payload["email"])
	# 	friends = Friendship.objects.all()
	# 	for friend in friends:
	# 		self.assertTrue(friend.friend.id == friend1.id or friend.friend.id == friend2.id)

	def test_user_with_email_exists_error(self):
		"""Test error returned if user with email exists."""
		payload = {
			"email" : "test@example.com",
			"password" : "testpass123",
			"first_name" : "Test",
			"last_name" : "Name",
		}
		create_user(**payload)
		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_too_short(self):
		""" expect that the user isn't created when the password is less than 5 characters"""
		payload = {
			"email" : "test@example.com",
			"password" : "pw",
			"first_name" : "Test",
			"last_name" : "Name",
		}
		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email=payload["email"]
		).exists()
		self.assertFalse(user_exists)

	def test_create_token_for_user(self):
		"""Test generates token for valid credentials."""
		user_details = {
			"name" : "Test Name",
			"email" : "test@example.com",
			"password" : "test-user-password123"
			"first_name" : "Test",
			"last_name" : "Name",
		}
		create_user(**user_details)
		payload = {
			"email" : user_details["email"],
			"password" : user_details["password"],
		}
		res = self.client.post(TOKEN_URL, payload)
		self.assertIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_create_token_bad_credentials(self):
		"""Test returns error if credentials invalid"""
		create_user(email="test@example.com", password="goodpass")
		payload={"email": "test@example.com", "password" : "wrongpass"}
		res = self.client.post(TOKEN_URL, payload)
		self.assertNotIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_blank_password(self):
		"""Test posting a blank password returns an error."""
		create_user(email="test@example.com", password="goodpass")
		payload = {"email" : "test@example.com", "password" : ""}
		res = self.client.post(TOKEN_URL, payload)
		self.assertNotIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_retrieve_user_unauthorized(self):
		""" Test authentication is required for users """
		res = self.client.get(ME_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
	""" Test API requests that require authentication. """

	def setUp(self):
		self.user = create_user(
			email="test@example.com",
			password="testpass123",
			first_name="Test",
			last_name="Name",
		)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_retrieve_profile_success(self):
		""" Test retrieving profile for logged in user """
		res = self.client.get(ME_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, {
			"email" : self.user.email,
			"first_name": self.user.first_name,
			"last_name": self.user.last_name,
		})

	def test_post_me_not_allowed(self):
		""" Test POST is not allowed for the me endpoint. """
		res = self.client.post(ME_URL, {})
		self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_update_user_profile(self):
		""" Test updating the user profile for the authenticated user. """
		payload = {"first_name" : "Updated", "last_name": "Name", "password" : "newpassword123"}

		# note the PATCH method for updating an existing entity
		res = self.client.patch(ME_URL, payload)
		# refresh from db to refresh the user's values after updating the values
		self.user.refresh_from_db()
		self.assertEqual(self.user.first_name, payload["first_name"])
		self.assertTrue(self.user.check_password(payload["password"]))
		self.assertEqual(res.status_code, status.HTTP_200_OK)

