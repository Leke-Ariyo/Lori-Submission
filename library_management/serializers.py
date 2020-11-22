from django.contrib import auth


from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','password','first_name','last_name' ,'is_active']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.is_active = True
        user.set_password(raw_password=validated_data.get('password'))
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        #fields = '__all__'
        fields = ['user']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','username','access_token', 'refresh_token', 'id']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')


        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')

        return {'email':user.email,'username':user.username,'access_token':user.tokens, 'refresh_token':user.refresh_tokens, 'id':user.pk, 'first_name':user.first_name,'last_name':user.last_name}



class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class BookToCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','name']

class CategorySerializer(serializers.ModelSerializer):
    book_category = BookToCatSerializer(many=True)
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = '__all__'


class BookLendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLending
        fields = '__all__'


class GetBookLendingSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    customer = CustomerSerializer()
    class Meta:
        model = BookLending
        fields = ('customer', 'book', 'date_logged', 'days_borrowed','rental_charge')



