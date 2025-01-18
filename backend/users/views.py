from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(APIView):
    """
    API View to handle Google OAuth2 login/register
    """

    @staticmethod
    def post(request):
        """
        Post method to authenticate a user using Google OAuth2 token.
        It expects an `access_token` in the request data.
        """
        serializer = GoogleSocialAuthSerializer(data=request.data)

        # Validate the provided Google access token
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
