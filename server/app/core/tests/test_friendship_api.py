from core.models import (
	User,
	Friendship,
	FriendRequest,
	FriendRequestStatus,
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

FRIENDSHIP_URL = reverse("core:friendship-list")
FRIEND_REQUEST_URL = reverse("core:friend-request-list")
FRIEND_REQUEST_HANDLE_URL = reverse("core:friendship-handle-friend-request")

def create_user(**params):
	""" Create and return a new user """
	return get_user_model().objects.create_user(**params)

class PrivateFriendshipApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = create_user(email="user@example.com", password="test123", first_name="Jansen", last_name="Yan")
		self.client.force_authenticate(self.user)

	def test_create_friendship(self):
		friend1 = create_user(email="friend1@example.com", password="test123") 

		payload = {
			"creator": self.user.id,
			"friend": friend1.id
		}	

		res = self.client.post(FRIENDSHIP_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.user.refresh_from_db()
		friends = self.user.get_friends().first()
		self.assertTrue(friends.creator.id == self.user.id and friends.friend.id == friend1.id)

	def test_create_friend_request(self):
		user1 = create_user(email="user2@example.com", password="test123")
		user2 = create_user(email="user3@example.com", password="test123")

		payload = {
			"from_user": user1.id,
			"to_user": user2.id,
		}

		res = self.client.post(FRIEND_REQUEST_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		incoming_friend_request = user2.get_incoming_friend_requests()
		self.assertIsNotNone(incoming_friend_request.first())
		self.assertEqual(incoming_friend_request.first().to_user.id, user2.id)

		outgoing_friend_request = user1.get_outgoing_friend_requests()
		self.assertIsNotNone(outgoing_friend_request.first())
		self.assertEqual(outgoing_friend_request.first().from_user.id, user1.id)

	def test_accept_friend_request(self):
		user1 = create_user(email="user2@example.com", password="test123")
		user2 = create_user(email="user3@example.com", password="test123")

		payload1 = {
			"from_user": user1.id,
			"to_user": user2.id,
		}

		# create friend request
		res = self.client.post(FRIEND_REQUEST_URL, payload1)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		incoming_friend_request = user2.get_incoming_friend_requests(status=FriendRequestStatus.PENDING)
		self.assertIsNotNone(incoming_friend_request.first())
		self.assertEqual(incoming_friend_request.first().to_user.id, user2.id)

		payload2 = {
			"id": incoming_friend_request.first().id,
			"status": FriendRequestStatus.ACCEPTED 
		}

		res = self.client.post(FRIEND_REQUEST_HANDLE_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

		# friend request should now be archived with the accepted_at date
		incoming_friend_request = user2.get_incoming_friend_requests(status=FriendRequestStatus.ACCEPTED)
		self.assertIsNotNone(incoming_friend_request.first())
		self.assertIsNotNone(incoming_friend_request.first().updated_at)

		# user1 and user2 should now be friends
		friendship = user2.get_friends().first()
		self.assertIsNotNone(friendship)
		self.assertEqual(friendship.friend, user2)
		self.assertEqual(friendship.creator, user1)

	def test_reject_friend_request(self):
		user1 = create_user(email="user2@example.com", password="test123")
		user2 = create_user(email="user3@example.com", password="test123")

		payload1 = {
			"from_user": user1.id,
			"to_user": user2.id,
		}

		# create friend request
		res = self.client.post(FRIEND_REQUEST_URL, payload1)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		incoming_friend_request = user2.get_incoming_friend_requests(status=FriendRequestStatus.PENDING)
		self.assertIsNotNone(incoming_friend_request.first())
		self.assertEqual(incoming_friend_request.first().to_user.id, user2.id)

		payload2 = {
			"id": incoming_friend_request.first().id,
			"status": FriendRequestStatus.REJECTED 
		}

		res = self.client.post(FRIEND_REQUEST_HANDLE_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

		# friend request should now be rejected with the updated_at date
		incoming_friend_request = user2.get_incoming_friend_requests(status=FriendRequestStatus.REJECTED)
		friend_request = incoming_friend_request.first()
		self.assertIsNotNone(friend_request)
		self.assertEqual(friend_request.status, FriendRequestStatus.REJECTED)
		self.assertIsNotNone(friend_request.updated_at)

		friendship = user1.get_friends().first()
		self.assertIsNone(friendship)

	def test_filter_friends_by_name(self):
		user1 = create_user(
			email="test2@example.com",
			first_name="Biggs",
			last_name="Brown",
			password="test123",
		)
		user2 = create_user(
			email="test3@example.com",
			first_name="Wedge",
			last_name="Brown",
			password="test123"
		)
		friendship1 = Friendship.objects.create(
			creator=user1,
			friend=self.user
		)
		friendship2 = Friendship.objects.create(
			creator=user2,
			friend=self.user
		) 

		res = self.client.get(FRIENDSHIP_URL + "?first_name=Biggs")
		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertEqual(len(res.data), 1)

		# the creator of the friendship should be Joe
		friend = User.objects.filter(id=res.data[0]["creator"])
		self.assertIsNotNone(friend.first())
		self.assertEqual(friend.first().first_name, "Biggs")

	def test_filter_friend_requests_by_status(self):
		user1 = create_user(
			email="test2@example.com",
			first_name="Biggs",
			last_name="Brown",
			password="test123",
		)
		user2 = create_user(
			email="test3@example.com",
			first_name="Wedge",
			last_name="Brown",
			password="test123"
		)
		payload = {
			"from_user": user1.id,
			"to_user": self.user.id,
		}
		payload2 = {
			"from_user": user2.id,
			"to_user": self.user.id
		}

		# create two friend requests
		res = self.client.post(FRIEND_REQUEST_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		res = self.client.post(FRIEND_REQUEST_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		res = self.client.get(FRIEND_REQUEST_URL +"?status=Pending")
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 2)
		friendship = res.data[0]
		self.assertEqual(friendship["status"], FriendRequestStatus.PENDING)

		payload2 = {
			"id": friendship["id"],
			"status": FriendRequestStatus.REJECTED 
		}

		# update the friend request status
		res = self.client.post(FRIEND_REQUEST_HANDLE_URL, payload2)
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

		# try to find pending status friendship, only one should be found 
		res = self.client.get(FRIEND_REQUEST_URL +"?status=Pending")
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		friendship = res.data[0]
		self.assertEqual(friendship["status"], FriendRequestStatus.PENDING)

		# rejected friend request should be found
		res = self.client.get(FRIEND_REQUEST_URL + "?status=Rejected")
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		friendship = res.data[0]
		self.assertEqual(friendship["status"], FriendRequestStatus.REJECTED)


