from rest_framework import serializers
from .models import *


from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'phone', 'password', 'password2')  

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': 'Parollar mos kelmadi!'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login = attrs.get("username", "")
        if '@' in login:
            user = User.objects.filter(email__iexact=login).first()
            if user:
                attrs['username'] = user.get_username()
        return super().validate(attrs)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'first_name', 'last_name', 
            'email', 'phone', 'avatar', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = '__all__'
