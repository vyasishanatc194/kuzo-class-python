# -*- coding: utf-8 -*-

from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from .response import MyAPIResponse
from core.utils import modify_api_response

# -----------------------------------------------------------------------------


class MyObtainAuthToken(ObtainAuthToken):
    """Override ObtainAuthToken to add in user ID."""

    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return MyAPIResponse(data={"user": user.pk, "token": token.key})


class MyAPIView(APIView):
    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)


class MyGenericAPIView(generics.GenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)


class MyUpdateAPIView(mixins.UpdateModelMixin, MyGenericAPIView):
    """UpdateAPIView
    UpdateModelMixin
    GenericAPIView
    APIView
    View
    """

    pass
