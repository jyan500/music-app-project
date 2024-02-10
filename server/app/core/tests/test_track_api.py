from core.models import (
	Artist,
	Genre,
	Track,
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from datetime import date

TRACK_URL = reverse("core:track-list")

def create_user(**params):
	""" Create and return a new user """
	return get_user_model().objects.create_user(**params)

class PrivateTrackApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = create_user(email="user@example.com", password="test123", first_name="Jansen",last_name="Yan")
		self.client.force_authenticate(self.user)

	# def test_create_song(self):
	# 	payload = {
	# 		"name":"Take 5",	
	# 		"artist": {
	# 			"name":"Dave Brubeck",	
	# 			"description": "Jazz Pianist",
	# 			"years_active": 4,
	# 		},
	# 		"genre": {
	# 			"name":"Jazz",	
	# 			"description": "jazz",	
	# 		},
	# 		"date": date.today()
	# 	}	
	# 	res = self.client.post(SONG_URL, payload, format="json")
	# 	song = res.data
	# 	self.assertIsNotNone(song)
	# 	self.assertEqual(song["name"], payload["name"])
	# 	self.assertEqual(song["genre"]["name"], payload["genre"]["name"])
	# 	self.assertEqual(song["artist"]["name"], payload["artist"]["name"])

	# def test_search_song(self):
	# 	payload = {
	# 		"name":"Take 5",	
	# 		"artist": {
	# 			"name":"Dave Brubeck",	
	# 			"description": "Jazz Pianist",
	# 			"years_active": 4,
	# 		},
	# 		"genre": {
	# 			"name":"Jazz",	
	# 			"description": "jazz",	
	# 		},
	# 		"date": date.today()
	# 	}	
	# 	res = self.client.post(SONG_URL, payload, format="json")
	# 	self.assertEqual(res.status_code, status.HTTP_201_CREATED)

	# 	payload2 = {
	# 		"name":"Giant Steps",	
	# 		"artist": {
	# 			"name":"John Coltrane",	
	# 			"description": "Jazz Saxophonist",
	# 			"years_active": 20,
	# 		},
	# 		"genre": {
	# 			"name":"Jazz",	
	# 			"description": "jazz",	
	# 		},
	# 		"date": date.today()
	# 	}	
	# 	res = self.client.post(SONG_URL, payload2, format="json")
	# 	self.assertEqual(res.status_code, status.HTTP_201_CREATED)

	# 	res = self.client.get(SONG_URL + "?name=Giant")
	# 	self.assertEqual(res.status_code, status.HTTP_200_OK)
	# 	song = res.data[0]
	# 	self.assertEqual(song["name"], payload2["name"])
	# 	self.assertEqual(song["artist"]["name"], payload2["artist"]["name"])
	# 	self.assertEqual(song["genre"]["name"], payload2["genre"]["name"])

	# 	res = self.client.get(SONG_URL + "?artist_name=Dave")
	# 	self.assertEqual(res.status_code, status.HTTP_200_OK)
	# 	song = res.data[0]
	# 	self.assertEqual(song["name"], payload["name"])
	# 	self.assertEqual(song["artist"]["name"], payload["artist"]["name"])
	# 	self.assertEqual(song["genre"]["name"], payload["genre"]["name"])



