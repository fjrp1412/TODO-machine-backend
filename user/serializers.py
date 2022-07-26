from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


# This class is a serializer for the User model. It has the fields id, email, name, and is_superuser.
# The password field is write only and has a minimum length of 8 characters
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'is_superuser', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """
        It takes the validated data and creates a user with the validated data

        :param validated_data: The data that has been validated by the serializer
        :return: The user model is being returned.
        """
        return get_user_model().objects.create_user(**validated_data)


# It takes the email and password from the request, authenticates the user, and then adds the user
# object to the validated data
class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        It takes the email and password from the request,
        authenticates the user,
        and then adds the user object to the validated data

        The validated data is then passed to the create function

        :param attrs: The validated data from the serializer
        :return: The user object is being returned.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs
