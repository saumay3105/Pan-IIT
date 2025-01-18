import os
import requests
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from .models import CustomUser


class CustomUserSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('full_name',)


class CustomRegisterSerializer(serializers.ModelSerializer):
    username = None
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # validate password according to Django's validators
        validate_password(attrs['password'])

        return super().validate(attrs)

    def save(self, request):
        validated_data = self.validated_data
        validated_data.pop('confirm_password')  # Remove confirm_password
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Set the password
        user.save()
        return user


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            id_info = id_token.verify_oauth2_token(auth_token, google_requests.Request())

            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            raise AuthenticationFailed('The token is either invalid or has expired: ' + str(e))


class GoogleSocialAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    access_token = serializers.CharField()

    def validate(self, attrs):
        user_data = Google.validate(attrs["id_token"])

        if user_data['aud'] != os.environ.get('GOOGLE_OAUTH_CLIENT_ID'):
            raise AuthenticationFailed('Wrong client')

        email = user_data['email']

        try:
            # Check if the user already exists
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            # Fetch user info from Google People API
            people_api_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
            response = requests.get(people_api_url, headers={"Authorization": f"Bearer {attrs['access_token']}"})
            response_data = response.json()

            # Extract name fields from People API response
            full_name = response_data.get('names', [{}])[0].get('displayName', '')

            # User does not exist, create a new user
            user = CustomUser.objects.create(email=email, full_name=full_name)
            user.full_name = full_name
            user.save()

        # Return tokens
        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
