from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import User
from dotenv import dotenv_values
import urllib.parse
import jwt

def index(request):
    users = User.objects.all().order_by("-max_velocity").values()
    template = loader.get_template("index.html")
    context = {
        "User": users,
    }
    return HttpResponse(template.render(context,request))

def data(request,slug):
    user = User.objects.get(id=slug)
    template = loader.get_template("data.html")
    context = {
        "user": user
    }
    return HttpResponse(template.render(context,request))

def getList(request):
    users = User.objects.all().order_by("-max_velocity").values()
    result = json.dumps(list(users),ensure_ascii=False,default=str)
    return JsonResponse(result,safe=False)

def getThrow(request, slug):
    try:
        user = User.objects.get(id=slug)
        result = {
            "id": user.id,
            "name": user.name,
            "max_velocity": user.max_velocity
        }
        result = json.dumps(result,ensure_ascii=False,default=str)
        return JsonResponse(result,safe=False)
    except:
        result = json.dumps({'error': '404'},ensure_ascii=False,default=str)
        return JsonResponse(result,safe=False)

def insertThrow(request):
    try:
        KEYS = dotenv_values()
        json_data = request.GET.get("payload")
        init = json.loads(urllib.parse.unquote(json_data))
        print(init)
        data = jwt.decode(init["jwt"],KEYS["JWT_SECRET"],algorithms=["HS256"])
        user = User(name=data.get("name"),max_velocity=data.get("max_velocity"))
        user.save()
        return JsonResponse(json.dumps([{'result':'success'}]),safe=False)
    except:
        return JsonResponse(json.dumps([{'result':'error happened!'}]),safe=False)