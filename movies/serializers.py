from rest_framework import serializers
from .models import RatingEnum, Movie, MovieOrder
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

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = MovieSerializer(read_only=True, source="movie")
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = UserSerializer(read_only=True, source="user")

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)