from django.contrib.auth import models
from rest_framework import fields, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.models import KSUser, Game, GameCategory, PaymentMethod, \
    Price, Order, Wishlist, Library
from api.exceptions import UsernameAlreadyExists

from django.contrib.auth.models import User


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
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'ksuser']

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email Already Exists!")
        return lower_email

    def create(self, validated_data):
        ksuser_data = validated_data.pop('ksuser')
        user = User.objects.create(**validated_data)
        KSUser.objects.create(user=user, **ksuser_data)
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
