from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers import UserSerializer
# from api.viewsets import UserViewSet


@method_decorator(csrf_exempt, name='UserCreate')
class UserCreate(viewsets.ModelViewSet):

    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)

    #     print(f"Serializer : {serializer}")
    #     # Define how would you like your response data to look like.
    #     response_data = {
    #         "success": "True",
    #         "message": "Successfully sent",
    #         "user": serializer.data
    #     }

    #     return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
