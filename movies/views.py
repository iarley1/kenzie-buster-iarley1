from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permission import IsSuperUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MoviesView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    def post(self, req: Request) -> Response:
        serializer = MovieSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=req.user)

        data = {
            "id": serializer.data["id"],
            "title": serializer.data["title"],
            "duration": serializer.data["duration"],
            "rating": serializer.data["rating"],
            "synopsis": serializer.data["synopsis"],
            "added_by": req.user.email
        }

        return Response(data, status.HTTP_201_CREATED)
    
    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, req)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
    
class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        
        serializer = MovieSerializer(movie)

        added_by = serializer.data["added_by"]

        email = added_by["email"]

        data = {
            "id": serializer.data["id"],
            "title": serializer.data["title"],
            "duration": serializer.data["duration"],
            "rating": serializer.data["rating"],
            "synopsis": serializer.data["synopsis"],
            "added_by": email
        }

        return Response(data, status.HTTP_200_OK)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieOrderSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=req.user, movie=movie)

        data = {
            "id": serializer.data["id"],
            "title": movie.title,
            "buyed_at": serializer.data["buyed_at"],
            "price": serializer.data["price"],
            "buyed_by": req.user.email
        }

        return Response(data, status.HTTP_201_CREATED)
