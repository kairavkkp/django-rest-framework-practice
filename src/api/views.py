from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics, serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import KSUser, PaymentMethod

from api.serializers import KSUserSerializer, UserSerializer


class UserCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            user_model = User.objects.get(
                username=request.data.__getitem__('username'))
            ksuser = KSUser.objects.create(
                user=user_model,
                bio=request.data['bio'],
                payment_method=None
            )
            ksuser.save()
            return Response(ksuser.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
