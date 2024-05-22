from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import connection
# Create your views here.

def loadhistory(request):
    user_id = request.GET.get("user_id")
    chatbot_id = request.GET.get("chatbot_id")
    with connection.cursor() as cursor:
        cursor.execute("select content, by_user, create_at from Chat_history where user_id = %s and chatbot_id = %s", [user_id,chatbot_id])
        row = cursor.fetchall()
    return JsonResponse({"data":row})


def newchat(request):
    # todo:加下filter或者其他的东西避免注入
    # 5/22 update:真的有必要吗，这个玩意好像就是参数化了
    input = request.GET.get("input")
    user_id = request.GET.get("user_id")
    chatbot_id = request.GET.get("chatbot_id")
    with connection.cursor() as cursor:
        cursor.execute("insert into chat_history values (%s,%s,NOW(),%s, 1);", [user_id,chatbot_id,input])
    # todo:丢到模型里产生输出
    output = "replace with openai output"
    with connection.cursor() as cursor:
        cursor.execute("insert into chat_history values (%s,%s,NOW(),%s, 0);", [user_id,chatbot_id,output])
    return JsonResponse({"data":output})