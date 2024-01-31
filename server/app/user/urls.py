"""
URL mappings for the user API.
"""
from django.urls import path
from user import views

app_name = "user"
# any requests made to the create/ will be handled the CreateUserView
# the as_view() allows us to convert our class based view into a function based view
# for the purposes of passing into this "path" function for the parameter
# the "name=create" is used for the reverse lookup (see test_user_api.py)
urlpatterns = [
	path("create/", views.CreateUserView.as_view(), name="create"),
	path("token/", views.CreateTokenView.as_view(), name="token"),
	path("me/", views.ManageUserView.as_view(), name="me")
]