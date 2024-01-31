"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
	UserSerializer,
	AuthTokenSerializer,
)
from rest_framework.response import Response
from rest_framework import status
import traceback

"""
	when the http request is made, it gets passed into this CreateUserView,
	which will then use the serializer to create the new user object 
""" 
class CreateUserView(generics.CreateAPIView):
	""" Create a new user in the system. """
	serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
	""" Create a new auth token for user """
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# the retrieveUpdateAPIView is specifically meant for HTTP GET AND PATCH/PUT
class ManageUserView(generics.RetrieveUpdateAPIView):
	""" Manage the authenticated user. """
	serializer_class = UserSerializer
	# token authentication to authenticate the user 
	authentication_classes = [authentication.TokenAuthentication]
	# only authenticated users can access this endpoint
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		""" Retrieve and return the authenticated user. """
		return self.request.user

