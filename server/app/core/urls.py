"""
URL mappings for the user API.
"""
from django.urls import (
	path,
	include,
)
import pprint
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
# create a new endpoint for /core 
router.register("friendship", views.FriendshipViewSet)
router.register("friend-request", views.FriendRequestViewSet, basename="friend-request")
router.register("artist", views.ArtistViewSet)
router.register("genre", views.GenreViewSet)
router.register("track", views.TrackViewSet)

app_name = "core"
# any requests made to the create/ will be handled the CreateUserView
# the as_view() allows us to convert our class based view into a function based view
# for the purposes of passing into this "path" function for the parameter
# the "name=create" is used for the reverse lookup (see test_user_api.py)
urlpatterns = [
	path("", include(router.urls))
]

pprint.pprint(router.get_urls())