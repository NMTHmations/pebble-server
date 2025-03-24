from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import User
from dotenv import dotenv_values
import urllib.parse
import jwt
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
import datetime


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
        "user": user,
        'alt_route': '../../' + user.video_source.__str__()
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
            "max_velocity": user.max_velocity,
            "distance": user.distance,
            "created_at": user.created_at
        }
        result = json.dumps(result,ensure_ascii=False,default=str)
        return JsonResponse(result,safe=False)
    except:
        result = json.dumps({'error': '404'},ensure_ascii=False,default=str)
        return JsonResponse(result,safe=False)

@api_view(['POST'])
def insertThrow(request):
    try:
        KEYS = dotenv_values()
        json_data = request.body.decode('utf-8')
        init = json.loads(urllib.parse.unquote(json_data))
        data = jwt.decode(init["jwt"],KEYS["JWT_SECRET"],algorithms=["HS256"])
        if not data:
            return JsonResponse(json.dumps([{'result':'Invalid request'}]),safe=False)
        user = User(name=data.get("name"),max_velocity=data.get("max_velocity"))
        user.save()
        return JsonResponse(json.dumps([{'result':'success'}]),safe=False)
    except:
        return JsonResponse(json.dumps([{'result':'error happened!'}]),safe=False)

class VideoUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, filename, format=None):
        try:
            if "file" not in request.FILES:
                return JsonResponse({'Response': 400, 'Message': 'No file provided'})
            file_obj = request.FILES["file"]
            file_extension = file_obj.name.split('.')[-1].lower()
            if file_extension != 'mp4':
                return JsonResponse({'Response': 400, 'Message': 'Invalid file format, only MP4 allowed'})
            lastUser = User.objects.all().get(id=len(User.objects.all().values()))
            if lastUser.video_source:
                return JsonResponse({'Response': 403, 'Message': 'A file has been uploaded already'})
            diff = datetime.datetime.now().timestamp() - lastUser.created_at.timestamp()
            if diff >= float(120):
                return JsonResponse({'Response':504,'Message': 'Timeout for video upload'})
            lastUser.video_source = file_obj
            lastUser.save()
            return JsonResponse({'Response': 204})
        except ObjectDoesNotExist:
            return JsonResponse({'Response': 404, 'Message': 'User not found'})
        except:
            return JsonResponse({'Response': 500})