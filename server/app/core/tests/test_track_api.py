from core.models import (
	Artist,
	Album,
	Genre,
	Track,
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from datetime import datetime

GENRE_URL = reverse("core:genre-list")
ALBUM_URL = reverse("core:album-list")
ARTIST_URL = reverse("core:artist-list")
TRACK_URL = reverse("core:track-list")

def create_user(**params):
	""" Create and return a new user """
	return get_user_model().objects.create_user(**params)

class PrivateTrackApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = create_user(email="user@example.com", password="test123", first_name="Jansen",last_name="Yan")
		self.client.force_authenticate(self.user)

	def test_create_song(self):
		## create genre and artists first, then the album
		genre_payload = {
			"name": "Bebop Jazz",
			"description": "Bebop Era of Jazz"
		}
		artist_payload = {
			"name": "John Coltrane",
			"description": "Jazz Alto Saxophonist",
			"years_active": 4	
		}
		album_payload = {
			"name": "Blue Train",
			"date": datetime.now().strftime("%Y-%m-%d"),
		}

		genre_res = self.client.post(GENRE_URL, genre_payload, format="json")
		artist_res = self.client.post(ARTIST_URL, artist_payload, format="json")
		album_res = self.client.post(ALBUM_URL, album_payload, format="json")

		album = Album.objects.filter(name="Blue Train").first()
		artist = Artist.objects.filter(name="John Coltrane").first()
		genre = Genre.objects.filter(name="Bebop Jazz").first()
		self.assertIsNotNone(album)
		self.assertIsNotNone(artist)
		self.assertIsNotNone(genre)

		album.artists.add(artist)
		album.genres.add(genre)

		album.refresh_from_db()

		all_artists = album.artists.all()
		all_genres = album.genres.all()

		self.assertEqual(len(all_artists), 1)
		self.assertEqual(len(all_genres), 1)

		self.assertEqual(all_artists[0].name, "John Coltrane")
		self.assertEqual(all_genres[0].name, "Bebop Jazz")

		track_payload = {
			"name": "Giant Steps",
			"date": datetime.now().strftime("%Y-%m-%d"),
			"album": album.id
		}

		track_response = self.client.post(TRACK_URL, track_payload, format="json")
		created_track = track_response.data

		album.refresh_from_db()

		all_tracks = album.tracks.all()
		self.assertEqual(len(all_tracks), 1)
		self.assertEqual(all_tracks[0].name, "Giant Steps")



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



