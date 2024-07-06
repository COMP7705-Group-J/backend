from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import connection
import threading
import openai
from openai import OpenAI
# Create your views here.

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .LTM_hunyuan import *
import datetime

import sys
sys.path.append("./")

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
    summary = get_last_summary(user_id, chatbot_id)
    print("summary is", summary)
    history_chat = get_history_chat(user_id, chatbot_id)
    update_prompt = generator_prompt.format(last_summary=summary)
    current_persona = get_current_persona(user_id, chatbot_id)
    persona_prompt = user_persona_prompt.format(current_persona = current_persona)
    history_chat.insert(0,{"Role": "system", "Content": update_prompt + persona_prompt + time_prompt})

    #print("history_chat", history_chat)
    
    api_key = get_api_key()
    # client = OpenAI(api_key=api_key)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = hunyuan_client.HunyuanClient(api_key, "ap-guangzhou", clientProfile)
    req = models.ChatCompletionsRequest()

    # prompt = "User: {}\nChatGPT: ".format(input)
    # history_chat = [{"role": "user", "content": prompt}]
    # chatGPT_input.append({"role": "user", "content": prompt})
    time_info = "Time: " + str(datetime.datetime.now()) + "\n"
    history_chat.append({"Role": "user", "Content": time_info + input})

    params = {
        "Model": "hunyuan-standard",
        "Messages": history_chat
    }
    #print(history_chat)
    req.from_json_string(json.dumps(params))
    response = client.ChatCompletions(req)
    output = response.Choices[0].Message.Content
    # output = "Hello, everlyn. How is today going?"
    with connection.cursor() as cursor:
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 1);", [user_id, chatbot_id, input])
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 0);", [user_id, chatbot_id, output])

    #异步更新总结
    thread_summary = threading.Thread(target=do_summary, args=(user_id, chatbot_id, summary, history_chat))
    thread_summary.start()

    thread_persona = threading.Thread(target=do_persona, args=(user_id, chatbot_id))
    thread_persona.start()

    return JsonResponse({"code":200,
                         "msg":"ok",
                         "data": output})