from core.models import (
	Artist,
	Genre
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

ARTIST_URL = reverse("core:artist-list")

def create_user(**params):
	""" Create and return a new user """
	return get_user_model().objects.create_user(**params)

class PrivateArtistApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = create_user(email="user@example.com", password="test123", first_name="Jansen",last_name="Yan")
		self.client.force_authenticate(self.user)

	def test_create_artist(self):
		payload = {
			"name":"Rob Araujo",	
			"description": "",
			"image": "",
			"years_active": 4,
		}	
		res = self.client.post(ARTIST_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		artist = Artist.objects.filter(name="Rob Araujo").first()
		self.assertEqual(artist.name, payload["name"])

	def test_search_artist(self):
		payload1 = {
			"name":"Rob Araujo",	
			"description": "Jazz Pianist - Hip Hop R&B",
			"image": "",
			"years_active": 4,
		}	
		res = self.client.post(ARTIST_URL, payload1)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		payload2 = {
			"name":"Miles Davis",	
			"image": "",
			"description": "Jazz Musician - Trumpet",
			"years_active": 20,
		}	
		res = self.client.post(ARTIST_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		res = self.client.get(ARTIST_URL + "?name=Miles")	
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data),  1)
		artist = res.data[0]

		self.assertEqual(artist["name"], payload2["name"])
		self.assertEqual(artist["description"], payload2["description"])
		self.assertEqual(artist["years_active"], payload2["years_active"])

		# case insensitive search
		res = self.client.get(ARTIST_URL + "?description=pianist")	
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data),  1)

		artist = res.data[0]

		self.assertEqual(artist["name"], payload1["name"])

