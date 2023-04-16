from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from .models import Movie
from .serializers import MovieSerializer
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return(request.user.is_authenticated and request.user.is_superuser)


class MoviesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]

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

        serialzier = MovieSerializer(movies, many=True)

        return Response(serialzier.data, status.HTTP_200_OK)
    
class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]

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