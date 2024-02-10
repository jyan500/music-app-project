from rest_framework import fields, serializers
from core.models import (
	Album,
	Artist,
	Friendship,
	FriendRequest,
	FriendRequestStatus,
	Genre,
	Playlist,
	Track,
	User
)
class FriendshipSerializer(serializers.ModelSerializer):
	creator = serializers.IntegerField(source="creator.id") 
	friend = serializers.IntegerField(source="friend.id")
	class Meta:
		model = Friendship
		fields = ["id", "creator", "friend", "created_at"]
		read_only_fields = ["created_at"]

	def create(self, validated_data):
		creator_id = validated_data.pop("creator")
		friend_id = validated_data.pop("friend")
		creator = None
		friend = None
		if creator_id:
			creator = User.objects.filter(id=creator_id["id"]).first()
		if friend_id:
			friend = User.objects.filter(id=friend_id["id"]).first()
		if creator and friend:
			friendship = Friendship.objects.create(creator=creator, friend=friend)
			return friendship

		return None


class FriendRequestSerializer(serializers.ModelSerializer):
	from_user = serializers.IntegerField(source="from_user.id")
	to_user = serializers.IntegerField(source="to_user.id")
	status = serializers.ChoiceField(choices=FriendRequestStatus.choices, required=False)
	created_at = serializers.DateTimeField(required=False)
	class Meta:
		model = FriendRequest
		fields = ["id", "from_user", "to_user", "created_at", "status"]
		read_only_fields = ["created_at"]

	def create(self, validated_data):
		from_user = validated_data.pop("from_user")
		to_user = validated_data.pop("to_user")
		if from_user:
			from_user = User.objects.filter(id=from_user["id"]).first()
		if to_user:
			to_user = User.objects.filter(id=to_user["id"]).first()
		if from_user and to_user:
			friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status=FriendRequestStatus.PENDING)
			return friend_request
		return None


class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = "__all__"
		read_only_fields = ["created_at"]

class ArtistSerializer(serializers.ModelSerializer):
	genres = GenreSerializer(many=True, required=False)
	class Meta:
		model = Artist
		fields = "__all__"
		read_only_fields = ["created_at"]

class AlbumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Album

class PlaylistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Playlist

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = "__all__"
		read_only_fields = ["created_at"]

	# def create(self, validated_data):
	# 	print("validated_data: ", validated_data)
	# 	created_artist = Artist.objects.create(**artist)
	# 	created_genre = Genre.objects.create(**genre)
	# 	track = Track.objects.create(**validated_data, artist=created_artist, genre=created_genre)
	# 	return track