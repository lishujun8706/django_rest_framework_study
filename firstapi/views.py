from django.shortcuts import render
from django.views import View
from django.contrib.auth import login,logout
from django.conf import settings
from django.http.response import HttpResponse,HttpResponseRedirect
import json
from django.http import JsonResponse
from rest_framework.views import  APIView
from firstapi.models import UserInfo, UserToken, Role,UserGroup
from firstapi.utils.auth import Authencation,SessionAuth
from firstapi.utils.my_permission import SVIPPermission,GeneralPermission
from firstapi.utils.my_throttling import DefineThrottling
from rest_framework.versioning import URLPathVersioning
from rest_framework.parsers import JSONParser,FormParser

def md5(user):
    import hashlib
    import time
    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))

    return m.hexdigest()

class OrderView(APIView):
    # authentication_classes = [Authencation,]
    # permission_classes = [SVIPPermission,]
    def post(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return JsonResponse({"code":1000,"msg":"order view","data":""})

class TestView(APIView):
    # authentication_classes = [SessionAuth,]
    # permission_classes = []
    throttle_classes = [DefineThrottling,]
    def get(self,request,*args,**kwargs):
        print("验证成功",request.user,request.auth.token)
        return HttpResponse(json.dumps({"code":1000,"msg":"test view","data":""}))

class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request,*args,**kwargs):
        try:
            username = request.GET.get("username",None)
            password = request.GET.get("password", None)
            usertype = request.GET.get("usertype", None)
            user = UserInfo.objects.update_or_create(username=username,defaults={"password":password,"user_type":int(usertype)})
            user = user[0]
            print(user.user_type)
            request.session[settings.UESR_SESSION_KEY] = user.id
            return HttpResponse(json.dumps({"code":1000,"msg":"success login","data":""}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"code": 1001, "msg": "failed login", "data": ""}))

    def post(self,request,*args,**kwargs):
        try:
            username = request.POST.get("username",None)
            password = request.POST.get("password", None)
            usertype = request.POST.get("usertype", None)
            user = UserInfo.objects.update_or_create(username=username,defaults={"password":password,"user_type":int(usertype)})
            user = user[0]
            request.session[settings.UESR_SESSION_KEY] = user.id
            return JsonResponse({"code": 1000, "msg": "success login", "data": ""})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 1001, "msg": "failed login", "data": ""})

# Create your views here.
class AuthView(APIView):
    authentication_classes = [] #赋空列表就不会再使用配置文件里的默认认证了
    permission_classes = [] #赋空列表就不会再使用配置文件里的默认权限设置了
    versioning_class = URLPathVersioning
    parser_classes = [JSONParser,FormParser]
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
            print(obj)
            print(request.session[settings.UESR_SESSION_KEY])
            print('.....>>>>>',request.version)
            #print('.....>>>>',version)
        else:
            request.session[settings.UESR_SESSION_KEY] = obj.id
        #############################################
        return HttpResponse(json.dumps({"code":1000,"msg":"good","data":None}))

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



#########################################################
from rest_framework import serializers

class RoleSerialize(serializers.Serializer):
    title = serializers.CharField()

class RoleView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request,*args,**kwargs):
        roles = Role.objects.all()
        ret = RoleSerialize(instance=roles,many=True)
        ret = json.dumps(ret.data,ensure_ascii=False)
        print("::::::::::::::::>>>>",ret)
        return HttpResponse(ret)

'''class UserInfoSerialize(serializers.Serializer):
    username = serializers.CharField()
    usertype = serializers.CharField(source="get_user_type_display")
    typeid = serializers.CharField(source="user_type")
    group = serializers.CharField(source="group.title")
    rsl = serializers.SerializerMethodField()

    def get_rsl(self,row):
        rol_obj_list = row.role.all()
        ret = []
        for item in rol_obj_list:
            ret.append({"id":item.id,"title":item.title})
        return ret'''
class UserInfoSerialize(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["id","username","password","group","role"]
        depth =1

class UserInfoView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,*args,**kwargs):
        users = UserInfo.objects.all()
        ret = UserInfoSerialize(instance=users,many=True)
        ret = json.dumps(ret.data,ensure_ascii=False)
        return HttpResponse(ret)