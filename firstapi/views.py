from django.shortcuts import render
from django.views import View
from django.contrib.auth import login,logout
from django.conf import settings
from django.http.response import HttpResponse,HttpResponseRedirect
import json
from django.http import JsonResponse
from rest_framework.views import  APIView
from firstapi.models import UserInfo, UserToken

def md5(user):
    import hashlib
    import time
    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))

    return m.hexdigest()

# class Authencation(object):
#     def authenticate(self,request):
#         token = request._request.GET.get("token")
#         user_token = UserToken.objects.filter(token=token).first()
#         if not user_token:
#             raise exceptions.AuthenticationFailed("验证失败")
#         return (user_token.user,user_token)
#
#     def authenticate_header(self,request):
#         pass

class OrderView(APIView):
    # authentication_classes = [Authencation,]
    def post(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return JsonResponse({"code":1000,"msg":"","data":""})


# Create your views here.
class AuthView(APIView):
    authentication_classes = [] #赋空列表就不会再使用配置文件里的默认认证了
    def get(self,request,*args,**kwargs):
        user = request.GET.get("username")
        pwd = request.GET.get("password")
        obj = UserInfo.objects.filter(username=user, password=pwd).first()
        #############验证session#####################
        if settings.UESR_SESSION_KEY in request.session.keys():
            # request.session["test1"] = "test1"
            # request.session["test2"] = "test2"
            # request.session["test3"] = "test3"
            #可存储多个key，但是都属于同一个用户；一个用户可以有多个session key
            print(request.session.keys())
            print(request.session[settings.UESR_SESSION_KEY])
        else:
            request.session[settings.UESR_SESSION_KEY] = obj.id
        #############################################
        return JsonResponse({"code":1000,"msg":"good","data":None})

    def post(self,request,*args,**kwargs):
        ret = {"code":1000,"msg":None}

        try:
            user = request.POST.get("username")
            pwd = request.POST.get("password")
            obj = UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret["code"] = 1001
                ret["msg"] = "用户名密码错误"
            token = md5(user)
            UserToken.objects.update_or_create(user=obj,defaults={'token':token})
        except Exception as e:
            print("登录错误",e)
            ret["code"] = 1001
            ret["msg"] = "error message"
            return JsonResponse(ret)

        return JsonResponse(ret)