from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings

from utils.mixins import ServiceExceptionHandlerMixin
from apps.authentication.permissions import JSONWebTokenAuthenticationMixin

from apps.authentication.services import (
    logout,
    get_user_data,
    change_user_password,
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginApi(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = data.get('user')
        token = data.get('token')

        full_data = get_user_data(user=user)

        response_data = jwt_response_payload_handler(token, user, request)
        response_data.update({'me': full_data})

        return Response(response_data)


class UserDetailApi(JSONWebTokenAuthenticationMixin, APIView):
    def get(self, request):
        full_data = get_user_data(user=self.request.user)

        return Response(full_data)


class LogoutApi(JSONWebTokenAuthenticationMixin, APIView):
    def post(self, request):
        logout(user=self.request.user)

        return Response(status=status.HTTP_202_ACCEPTED)


class ChangePasswordApi(
    ServiceExceptionHandlerMixin,
    JSONWebTokenAuthenticationMixin,
    APIView
):
    class Serializer(serializers.Serializer):
        old_password = serializers.CharField()
        new_password = serializers.CharField()

    def post(self, request):
        serializer = self.Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['user'] = self.request.user

        change_user_password(**data)

        return Response(status=status.HTTP_202_ACCEPTED)
