from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import RegisterSerializer, UserSerializer

# Create your views here.
class User(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "message": "Users retrieved successfully.",
            "users": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors, "user": []}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "User logged out successfully."   
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "error": "Invalid token or token has already been blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)