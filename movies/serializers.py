from rest_framework import serializers
from .models import RatingEnum, Movie
from users.serializers import UserSerializer

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default=None)
    rating = serializers.ChoiceField(
        choices=RatingEnum.choices,
        default=RatingEnum.G,
    )
    synopsis = serializers.CharField(default=None)
    added_by = UserSerializer(read_only=True, source="user")

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)
