from django.conf import settings
from firstapi.models import UserInfo, UserToken
from rest_framework import exceptions
from rest_framework.authentication import  BaseAuthentication

class Authencation(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get("token")
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            raise exceptions.AuthenticationFailed("验证失败")
        return (user_token.user,user_token)

    def authenticate_header(self,request):
        pass