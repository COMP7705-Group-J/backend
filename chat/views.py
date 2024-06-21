from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import connection
import openai
from openai import OpenAI
# Create your views here.

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from LTM import get_api_key

def list_chat(request):
    user_id = request.GET.get("user_id")
    with connection.cursor() as cursor:
        cursor.execute("Select chatbot_id, chatbot_name, create_at, content\
                        From (\
                            Select Chat_history.chatbot_id, ChatBot.chatbot_name, Chat_history.create_at, Chat_history.content, ROW_NUMBER() \
                                Over (Partition By Chat_history.chatbot_id Order By Chat_history.create_at Desc) As rn\
                            From Chat_history \
                            Left Join ChatBot\
                            On Chat_history.chatbot_id = ChatBot.chatbot_id\
                            Where Chat_history.user_id = %s And ChatBot.is_deleted = False\
                            ) As subquery\
                        Where rn = 1 Order By create_at Desc", [user_id])
        row = cursor.fetchall()
    return JsonResponse({"code":200,
                         "msg":"ok",
                         "data":row})

def loadhistory(request):
    user_id = request.GET.get("user_id")
    chatbot_id = request.GET.get("chatbot_id")
    with connection.cursor() as cursor:
        cursor.execute("select content, by_user, create_at from Chat_history where user_id = %s and chatbot_id = %s", [user_id,chatbot_id])
        row = cursor.fetchall()
    return JsonResponse({"code":200,
                         "msg":"ok",
                         "data":row})

# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def newchat(request):
    input = request.POST.get("input")
    user_id = request.POST.get("user_id")
    chatbot_id = request.POST.get("chatbot_id")  
    with connection.cursor() as cursor:
        cursor.execute("select content, by_user, create_at from Chat_history where user_id = %s and chatbot_id = %s Order By create_at", [user_id,chatbot_id])
        row = cursor.fetchall()
    history_chat = []
    generator_prompt = "consider the history chat content and give the correspond answer"
    history_chat.append({"role": "system", "content" : generator_prompt})
    for i in range(len(row)):
        if row[i][1]:
            history_chat.append({"role": "user", "content" : row[i][0]})
        else:
            history_chat.append({"role": "assistant","content" : row[i][0]})
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    # prompt = "User: {}\nChatGPT: ".format(input)
    # history_chat = [{"role": "user", "content": prompt}]
    # chatGPT_input.append({"role": "user", "content": prompt})
    history_chat.append({"role": "user", "content": input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=history_chat
    )

    output = response.choices[0].message.content

    with connection.cursor() as cursor:
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 1);", [user_id, chatbot_id, input])
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 0);", [user_id, chatbot_id, output])

    return JsonResponse({"code":200,
                         "msg":"ok",
                         "data": output})