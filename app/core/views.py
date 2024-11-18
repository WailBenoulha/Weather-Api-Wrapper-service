from django.shortcuts import render

# settings for rest framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# settings for redis
import requests
import redis

from django.conf import settings
from django.http import JsonResponse

redis_client = redis.StrictRedis(host='localhost',port=6379,db=0, decode_responses=True)

@api_view(['GET'])
def index(request,city):
    redis_key = f"weather:{city}"
    cached_data = redis_client.get(redis_key)
    if cached_data:
        return Response(eval(cached_data))
    url ='https://api.openweathermap.org/data/2.5/weather?q={}&appid=c4963a5e7e419dc7a5a9d8952645e7ed'
    
    r = requests.get(url.format(city))
    if r.status_code == 200:
        data = r.json()
        redis_client.setex(redis_key,600,str(data))
        return Response(data)
    else:
        return Response({"error":"Failed to fetch weather data"})