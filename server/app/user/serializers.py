"""
Serializers for the user API View.
"""
from django.contrib.auth import (
	get_user_model,
	authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import (
	Friendship,
	FriendRequest,
	User
)

"""
Notes:
takes objects and parses and validates the data that can be used to display in JSON
or convert user input back to python object/model

there are different base classes available for serializers:
serializers.Serializer
serializers.ModelSerializer allow us to automatically validate and save things to
a specific model that we define in our serializer via the "model" attribute under the "Meta" class

the "fields" attribute defines values that we want to make available to the serializer (i.e what fields
are available in the request, and can be changed). For example, email, password and name are the only
fields that we want users to be able to change

the "extra_kwargs" is a dictionary to provide additional metadata
i.e write_only: user will be able to set the value, but won't be able to see it in the api response for security
min_length: minimum length of the value in order to be considered valid (if not valid, returns 400 response)
"""



class UserSerializer(serializers.ModelSerializer):
	""" Serializer for the user object. """
	# friends = FriendSerializer(many=True, required=False)

	class Meta:
		model = get_user_model()
		# fields = ["email", "password", "name", "friends"]
		fields = ["email", "password", "first_name", "last_name"]
		extra_kwargs = {"password": {"write_only" : True, "min_length" : 5}}

	# def _get_or_create_friends(self, user, friends):
	# 	# if the user is not friends with this user, add them
	# 	for friend in friends:
	# 		friend_id = friend["friend"]["id"]
	# 		friend = User.objects.get(id=friend_id)
	# 		Friendship.objects.get_or_create(
	# 			creator=user,
	# 			friend=friend
	# 		)

	def create(self, validated_data):
		"""Create and return a user with encrypted password."""
		# friends = validated_data.pop("friends", [])
		user = get_user_model().objects.create_user(**validated_data)
		# self._get_or_create_friends(user, friends)
		# friendships = Friendship.objects.all()
		return user

	def update(self, instance, validated_data):
		"""Update and return user"""
		# remove the password from the validated data (so it doesn't get included below in the super().update)
		# defaults to None because we don't require this field to be input
		password = validated_data.pop("password", None)
		# perform the update from the ModelSerializer's update method
		user = super().update(instance, validated_data)
		if password:
			user.set_password(password)
			user.save()
		return user

class AuthTokenSerializer(serializers.Serializer):
	""" Serializer for the user auth token. """
	email = serializers.EmailField()
	password = serializers.CharField(
		# make the text hidden
		style={"input type": "password"},
		trim_whitespace=False,
	)

	def validate(self, attrs):
		""" Validate and authenticate the user. """
		email = attrs.get("email")
		password = attrs.get("password")
		user = authenticate(request=self.context.get("request"), username=email, password=password)

		if not user:
			msg = _("Unable to authenticate with provided credentials.")
			raise serializers.ValidationError(msg, code="authorization")

		attrs["user"] = user
		return attrs



