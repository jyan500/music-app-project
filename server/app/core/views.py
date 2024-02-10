from drf_spectacular.utils import (
	extend_schema_view,
	extend_schema,
	OpenApiParameter,
	OpenApiTypes,
)
from rest_framework import (
	viewsets,
	mixins,
	status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
	Artist,
	Friendship,
	FriendRequest,
	FriendRequestStatus,
	Genre,	
	Track,
	User,
)
from django.db import models
from rest_framework.exceptions import NotFound
from core import serializers
from datetime import datetime

class FriendshipViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.FriendshipSerializer
	queryset = Friendship.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		# filter friends by...
		# name
		first_name = self.request.query_params.get("first_name")
		last_name = self.request.query_params.get("last_name")
		user = self.request.user
		queryset = self.queryset
		queryset = queryset.filter(models.Q(creator=user)|models.Q(friend=user))
		if first_name:
			queryset = queryset.filter(models.Q(friend__first_name__icontains=first_name) | models.Q(creator__first_name__icontains=first_name))
		if last_name:
			queryset = queryset.filter(models.Q(friend__last_name__icontains=last_name) | models.Q(creator__last_name__icontains=last_name))
		return queryset

	# either accept or reject a friend request
	@action(detail=False, methods=["post"])
	def handle_friend_request(self, request):
		# find the friend request based on the request's id
		data = request.data
		friend_request_id = data.get("id")
		friend_request_status = data.get("status")
		friend_request = FriendRequest.objects.filter(id=friend_request_id).first()
		if friend_request:
			from_user = User.objects.filter(id=friend_request.from_user.id).first()
			to_user = User.objects.filter(id=friend_request.to_user.id).first()
			if (from_user and to_user):
				if (friend_request_status == FriendRequestStatus.ACCEPTED):
					# create friendship
					# normally on serializers, you return the model and then the default view method
					# will call save on that, but on custom views, you need to call save manually
					Friendship.objects.create(creator=from_user, friend=to_user)

				friend_request.status = friend_request_status 
				friend_request.updated_at = datetime.now()
				friend_request.save()

		else:
			return Response(error="friend request not found", status=status.HTTP_400_BAD_REQUEST) 
		return Response(status=status.HTTP_204_NO_CONTENT)

class FriendRequestViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.FriendRequestSerializer
	queryset = FriendRequest.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		# filter friend requests by...
		# status
		queryset = self.queryset
		user = self.request.user
		status = self.request.query_params.get("status")
		queryset = queryset.filter(models.Q(from_user=user)|models.Q(to_user=user))
		if status:
			for status_label in FriendRequestStatus.names:
				if status.upper() == status_label:
					queryset = queryset.filter(status=FriendRequestStatus[status_label])
					break
		return queryset.order_by("created_at")

class ArtistViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ArtistSerializer
	queryset = Artist.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = self.queryset
		name = self.request.query_params.get("name")
		years_active = self.request.query_params.get("years_active")
		description = self.request.query_params.get("description")

		if name:
			queryset = queryset.filter(name__icontains=name)
		if years_active:
			queryset = queryset.filter(years_active=years_active)
		if description:
			queryset = queryset.filter(description__icontains=description)

		return queryset.order_by("name")

class GenreViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.GenreSerializer
	queryset = Genre.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = self.queryset
		name = self.request.query_params.get("name")
		description = self.request.query_params.get("description")

		if name:
			queryset = queryset.filter(name__icontains=name)
		if description:
			queryset = queryset.filter(description__icontains=description)

		return queryset.order_by("name")

class TrackViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.TrackSerializer
	queryset = Track.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = self.queryset
		name = self.request.query_params.get("name")
		artist_name = self.request.query_params.get("artist_name")
		genre_name = self.request.query_params.get("genre_name")

		if name:
			queryset = queryset.filter(name__icontains=name)
		# if artist_name:
		# 	queryset = queryset.filter(artist__name__icontains=artist_name)
		# if genre_name:
		# 	queryset = queryset.filter(genre__name__icontains=genre_name)

		return queryset.order_by("name")

