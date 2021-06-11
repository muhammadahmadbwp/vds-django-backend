from rest_framework import serializers
from users.models import UserProfile
from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token

# Serializers define the API representation.

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.is_active = validated_data.pop('is_active', instance.is_active)
        instance.save()
        return instance

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'name', 'telephone', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        if Token.objects.filter(user=obj).exists():
            token = Token.objects.get(user=obj)
        else:
            token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    print('before')

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value