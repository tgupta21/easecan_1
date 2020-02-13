from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import Merchant
from directory.models import Directory


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('phone', 'email', 'password', 'user_type')
        read_only_fields = ('user_type',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class MerchantSerializer(serializers.ModelSerializer):
    """Serializer for the merchant object"""
    user = UserSerializer(required=True)

    class Meta:
        model = Merchant
        exclude = ['is_verified']

    def create(self, validated_data):
        """Create a new merchant with encrypted password and return it"""
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.user_type = 2
        merchant = Merchant.objects.create(user=user, **validated_data)
        return merchant


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=phone,
            password=password
        )
        if not user:
            msg = 'Invalid credentials'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
