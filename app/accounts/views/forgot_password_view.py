from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.serializers import ForgotPasswordRequestSerializer, ResetPasswordSerializer
from accounts.models import ForgotPassword
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
import os

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        print(os.environ.get('DEFAULT_FROM_EMAIL'))
        print(os.environ.get('EMAIL_HOST'))
        print(os.environ.get('EMAIL_PORT'))
        print(os.environ.get("EMAIL_BACKEND"))
        print(os.environ.get("EMAIL_USE_TLS"))
        print(os.environ.get("EMAIL_USE_SSL"))
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = ForgotPassword(email=email, token=token)
            reset.save()

            # Send Email logic here
            send_mail(
                subject='Password Reset Request',
                message=f'Use the following token to reset your password: {token}',
                from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({
                "success": True,
                "message": "We have sent you a link to reset your password.",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "No user is associated with this email address."
            }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_obj = ForgotPassword.objects.filter(token=token).first()

        if not reset_obj:
            return Response({
                "success": False,
                "message": "Invalid or expired token."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email__iexact=reset_obj.email).first()

        if user:
            user.set_password(request.data['new_password'])
            user.save()

            reset_obj.delete()

            return Response({
                "success": True,
                "message": "Password has been reset successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "User not Found"
            }, status=status.HTTP_400_BAD_REQUEST)
