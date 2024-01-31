"""
Database Models
"""
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin
)
from django.utils.translation import gettext_lazy as _

class FriendRequestStatus(models.TextChoices):
	REJECTED = 'REJECTED', _('Rejected')
	ACCEPTED = 'ACCEPTED', _('Accepted')
	PENDING = 'PENDING', _('Pending')

class UserManager(BaseUserManager):
	""" Manager for users """

	def create_user(self, email, password=None, **extra_fields):
		""" Create, save and return a new user. """
		if not email:
			raise ValueError("User must have an email address")
		user = self.model(email=self.normalize_email(email), **extra_fields)
		## password hash
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		""" Create and return a new superuser"""
		user = self.create_user(email, password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user

class User(AbstractBaseUser, PermissionsMixin):
	"""User in the system."""
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	def get_friends(self):
		return Friendship.objects.filter(models.Q(creator=self.pk)|models.Q(friend=self.pk))

	def get_incoming_friend_requests(self, status=FriendRequestStatus.PENDING):
		return FriendRequest.objects.filter(to_user=self.pk, status=status)

	def get_outgoing_friend_requests(self, status=FriendRequestStatus.PENDING):
		return FriendRequest.objects.filter(from_user=self.pk, status=status)
	
	def get_friend_by_id(self, friend_id):
		return Friendship.objects.filter(models.Q(creator=friend_id) | models.Q(friend=friend_id))


	objects = UserManager()

	USERNAME_FIELD = "email"

class Friendship(models.Model):
	creator = models.ForeignKey(User, related_name="friendship_creator", on_delete=models.CASCADE)
	friend = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

	def __str__(self):
		return f'{self.creator} {self.friend}'

class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE) 
	to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(null=True, blank=True)

	status = models.CharField(
        max_length=50,
        choices=FriendRequestStatus.choices,
        default=FriendRequestStatus.PENDING,
    )


class Artist(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	years_active = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

class Genre(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

class Song(models.Model):
	name = models.CharField(max_length=255)
	date = models.DateField()
	artist = models.ForeignKey(Artist, related_name="artist", on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre, related_name="song_genre", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

class Album(models.Model):
	name = models.CharField(max_length=255)
	date = models.DateField()
	genre = models.ForeignKey(Genre, related_name="album_genre", on_delete=models.CASCADE)
	songs = models.ManyToManyField(Song)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

	class AlbumType(models.TextChoices):
		SINGLE = 'SINGLE', _('Single')
		COMPILATION = 'COMPILATION', _('Compilation')

	album_type = models.CharField(
        max_length=50,
        choices=AlbumType.choices,
        default=AlbumType.COMPILATION,
    )

class Playlist(models.Model):
	name = models.CharField(max_length=255)
	creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
	collaborators = models.ManyToManyField(User)
	songs = models.ManyToManyField(Song)
	views = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

