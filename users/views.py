from rest_framework.views import APIView, Response, Request, status
from .serializers import UserSerializer
from .models import User


class UsersView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
