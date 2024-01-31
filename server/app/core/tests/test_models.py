from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models
from datetime import datetime

class ModelTests(TestCase):
	""" Test models """

	def test_create_user_with_email_successful(self):
		""" Test creating a user with an email is successful """
		email = "test@example.com"
		password = "testpass123"
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)
		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""Test email is normalized for new users."""
		sample_emails = [
			["test1@EXAMPLE.com", "test1@example.com"],
			["Test2@Example.com", "Test2@example.com"],
			["TEST3@Example.com", "TEST3@example.com"],
			["test4@Example.COM", "test4@example.com"],
		]	
		for email, expected in sample_emails:
			user = get_user_model().objects.create_user(email, "sample123")
			self.assertEqual(user.email, expected)

	def test_new_user_without_email_raises_error(self):
		"""Test that creating a user without an email raises a ValueError."""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user("", "test123")

	def test_create_superuser(self):
		"""Test creating a superuser."""
		user = get_user_model().objects.create_superuser(
			"test@example.com",
			"test123"
		)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)

	def test_add_friend(self):
		user1 = get_user_model().objects.create_user(
			"test1@example.com",
			"test123"
		)
		user2 = get_user_model().objects.create_user(
			"test2@example.com",
			"test123"
		)
		friend_request = models.FriendRequest.objects.create(
			from_user=user1,
			to_user=user2
		)
		to_user2 = models.FriendRequest.objects.filter(to_user=user2).first()
		# user 2 accepts

		friendship = models.Friendship.objects.create(
			creator=user1,
			friend=user2
		)

		# user 2 is now friends with user 1, and vice versa
		user2_friendship = user2.get_friends().first()
		user1_friendship = user1.get_friends().first()

		self.assertTrue(user2_friendship.creator == user2 or user2_friendship.friend == user2)
		self.assertTrue(user1_friendship.creator == user1 or user2_friendship.friend == user1)

		# after user accepts, friend request is deleted
		to_user2.delete()

		# attempt to find the friend request, but it should no longer be there
		to_user2 = models.FriendRequest.objects.filter(to_user=user2).first()
		self.assertEqual(to_user2, None)

	def test_add_song(self):
		genre = models.Genre.objects.create(
			name="Jazz",
			description="Modern Jazz"
		)
		artist = models.Artist.objects.create(
			name="Rob Araujo",	
			description="",
			years_active=4,
		)
		song = models.Song.objects.create(
			name="Nineteen",
			date=datetime.now(),
			artist=artist,
			genre=genre
		)

		self.assertTrue(models.Song.objects.filter(name="Nineteen").count(), 1)

	def test_add_album(self):
		genre1 = models.Genre.objects.create(
			name="Jazz",
			description="Modern Jazz"
		)
		genre2 = models.Genre.objects.create(
			name="R&B",
			description="R&B"
		)
		artist = models.Artist.objects.create(
			name="Rob Araujo",	
			description="",
			years_active=4,
		)
		song1 = models.Song.objects.create(
			name="Nineteen",
			date=datetime.now(),
			artist=artist,
			genre=genre1
		)
		song2 = models.Song.objects.create(
			name="River",
			date=datetime.now(),
			artist=artist,
			genre=genre2,
		)
		song3 = models.Song.objects.create(
			name="Moon Rock",
			date=datetime.now(),
			artist=artist,
			genre=genre1
		)
		album = models.Album.objects.create(
			name="Nineteen (Release)",
			date=datetime.now(),
			genre=genre1
		)
		album.songs.add(song1, song2, song3)
		album.save()

		album.refresh_from_db()
		created_album = models.Album.objects.filter(name="Nineteen (Release)")
		self.assertEqual(created_album.count(), 1)
		self.assertEqual(created_album.first().songs.count(), 3)

	def test_add_playlist(self):
		user1 = get_user_model().objects.create_user(
			"test1@example.com",
			"test123"
		)
		user2 = get_user_model().objects.create_user(
			"test2@example.com",
			"test123"
		)
		genre1 = models.Genre.objects.create(
			name="Jazz",
			description="Modern Jazz"
		)
		genre2 = models.Genre.objects.create(
			name="R&B",
			description="R&B"
		)
		artist = models.Artist.objects.create(
			name="Rob Araujo",	
			description="",
			years_active=4,
		)
		song1 = models.Song.objects.create(
			name="Nineteen",
			date=datetime.now(),
			artist=artist,
			genre=genre1
		)
		song2 = models.Song.objects.create(
			name="River",
			date=datetime.now(),
			artist=artist,
			genre=genre2,
		)
		song3 = models.Song.objects.create(
			name="Moon Rock",
			date=datetime.now(),
			artist=artist,
			genre=genre1
		)
		playlist = models.Playlist.objects.create(
			name="My Jazz Playlist",
			creator=user1,
		)
		playlist.collaborators.add(user2)
		playlist.songs.add(song1, song2, song3)
		playlist.views = 1
		playlist.save()




