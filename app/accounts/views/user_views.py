from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.serializers import UserSerializer

# Create your views here.
class User(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors, "user": []}, status=status.HTTP_400_BAD_REQUEST)