from django.contrib.auth import authenticate, models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import fields, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.models import KSUser, Game, GameCategory, PaymentMethod, \
    Price, Order, Wishlist, Library
from api.exceptions import UsernameAlreadyExists

from api.utils import validateEmail


# Help from :
# https://stackoverflow.com/questions/28058326/django-rest-framework-obtain-auth-token-using-email-instead-username
class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User, email=email_or_username
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationError(msg)
        else:
            msg = 'Must include "email or username" and "password"'
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs


class PaymentMethodSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=15)
    customer_id = serializers.CharField(
        max_length=20, allow_null=True, allow_blank=True)

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class KSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSUser
        fields = ['bio', 'payment_method']


class UserSerializer(serializers.ModelSerializer):
    ksuser = KSUserSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'ksuser']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email Already Exists!")
        return lower_email

    def create(self, validated_data):
        ksuser_data = validated_data.pop('ksuser')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.active = True
        user.staff = False
        user.admin = False
        user.save()
        ksuser = KSUser.objects.create(user=user, **ksuser_data)
        ksuser.save()
        return user


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
