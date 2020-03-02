from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework_jwt import authentication

from accounts.permissions import IsSuperUser
from accounts.serializers import UserTokenSerializer,UserSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



global User
User = get_user_model()


class GetUserToken(generics.GenericAPIView):
    """
    get the new user token
    token can access only superuser
    """
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    serializer_class = UserTokenSerializer
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception =  True)
        user = User.objects.get(pk=serializer.data['userID'])
        payload = jwt_payload_handler(user)

        token = jwt_encode_handler(payload)
        return Response({'token': token})
        # return Response(serializer.data)





class UserList(APIView):
    """
    View to list all users in the system.
    * Requires token authentication.
    * Only Super users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.JSONWebTokenAuthentication]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class UsersDetail(APIView):
    """
    Retrieve, update or delete a User.
    """
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    User = get_user_model()

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response('Successfully deleted')
