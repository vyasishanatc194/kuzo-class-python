from core.api.permissions import IsSuperUser
from core.api.viewsets import MyModelViewSet
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveAPIView,UpdateAPIView
from core.api.serializers import UserSerializer, MyUserSerializer
from core.api.pagination import CustomPagination

from twilio.rest import Client
import re

from django.utils import timezone
from datetime import datetime, timedelta, date

from core.api.apiviews import MyAPIView, MyListAPIView

from core.api.serializers import UserDetailsSerializer, UserUpdateDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.utils import modify_api_response

# ........................................................................................
# API For Profile
# ........................................................................................


class UserDetailsView(MyListAPIView):

    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        name = self.request.query_params.get("name", None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ProfileDetailsView(MyAPIView):

    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        GET method for retrieving the data
        """

        try:
            user = get_user_model().objects.get(pk=pk)
            if user is not None:
                serializer = UserDetailsSerializer(user, context={"request": request})
                return Response({"status": "OK", "message": "Successfully fetched user details", "data": serializer.data})

        except get_user_model().DoesNotExist:
            return Response({"status": "FAIL", "message": "User not found", "data": []})


class ProfileUpdateView(MyAPIView):
    
    queryset = get_user_model().objects.all()
    serializer_class = UserUpdateDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        """
        PUT method to update the data
        """

        if request.user.is_authenticated:

            user_check = get_user_model().objects.filter(pk=pk).exists()

            if not user_check:
                return Response({"status": "FAIL", "message": "User not found", "data": []})

            user = get_user_model().objects.get(pk=pk)

            serializer = UserUpdateDetailsSerializer(user, data=request.data, partial=True, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response({"status": "OK", "message": "Successfully updated user", "data": serializer.data})

            else:
                return Response({"status": "FAIL", "message": "Serializer validation error", "data": serializer.errors})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})
