from core.models import (
	Genre
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

GENRE_URL = reverse("core:genre-list")

def create_user(**params):
	""" Create and return a new user """
	return get_user_model().objects.create_user(**params)

class PrivateGenreApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = create_user(email="user@example.com", password="test123", first_name="Jansen",last_name="Yan")
		self.client.force_authenticate(self.user)

	def test_create_genre(self):
		payload = {
			"name":"Jazz",	
			"description": "jazz",
		}	
		res = self.client.post(GENRE_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		genre = Genre.objects.filter(name="Jazz").first()
		self.assertEqual(genre.name, payload["name"])

	def test_search_genre(self):
		payload = {
			"name":"Jazz",	
			"description": "jazz",
		}	
		res = self.client.post(GENRE_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		genre = Genre.objects.filter(name="Jazz").first()
		self.assertEqual(genre.name, payload["name"])

		payload2 = {
			"name":"Hip Hop",	
			"description": "jazz hip hop",
		}	
		res = self.client.post(GENRE_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		genre = Genre.objects.filter(name="Hip Hop").first()
		self.assertEqual(genre.name, payload2["name"])

		res = self.client.get(GENRE_URL + "?description=jazz")
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 2)
		self.assertEqual(res.data[0]["description"], "jazz hip hop")
		self.assertEqual(res.data[1]["description"], "jazz")


