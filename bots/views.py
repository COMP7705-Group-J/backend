from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import connection

from datetime import datetime
import time

# Create your views here.
GENERAL = 0
CUSTOMIZABLE = 1

persona = [
    "Jay Chou",
    "Jackie Chan",
    "Defined by me"
]


def get_persona(request):
    return JsonResponse({"code": 200,
                         "msg": "OK",
                         "data": persona})


def create(request):
    data = request.POST
    # TODO 检查用户登陆状态
    user_id = data.get("user_id")
    chatbot_id = generate_unique_id()
    chatbot_name = data.get("chatbot_name")
    chatbot_type = int(data.get("chatbot_type"))
    chatbot_persona = ""
    if chatbot_type == CUSTOMIZABLE:
        chatbot_persona = data.get("chatbot_persona")
    is_deleted = 0
    code = 200
    msg = "OK"
    # TODO 检查重复创建
    data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into ChatBot values (%s, %s, %s, %s, %s, NOW(),%s);", [user_id, chatbot_id, chatbot_name,
                                                                               chatbot_type, chatbot_persona,
                                                                               is_deleted])
            data.append({"chatbot_id": chatbot_id})
    except Exception as e:
        code = -1
        msg = str(e)

    return JsonResponse({"code": code,
                         "msg": msg,
                         "data": data})


# TODO
def generate_unique_id():
    # 获取当前时间戳
    current_time = int(time.time()) % (2 ** 16 - 1)

    return current_time


def detail(request):
    data = request.POST
    # TODO 检查用户登陆状态
    user_id = data.get("user_id")
    chatbot_id = data.get("chatbot_id")
    code = 200
    msg = "OK"
    data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from ChatBot where user_id=%s and chatbot_id=%s and is_deleted=0;",
                           [user_id, chatbot_id])
            result = cursor.fetchall()
            if len(result) > 0:
                for row in result:
                    data.append({
                        "chatbot_name": row[2],
                        "chatbot_type": row[3],
                        "chatbot_persona": row[4],
                        "create_at": row[5]
                    })
            else:
                code = -1
                msg = "DetailsNotFound"

    except Exception as e:
        code = -1
        msg = str(e)
        # print(msg)

    return JsonResponse({"code": code,
                         "msg": msg,
                         "data": data})


def list(request):
    data = request.POST
    # TODO 检查用户登陆状态
    user_id = data.get("user_id")
    code = 200
    msg = "OK"
    data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from ChatBot where user_id=%s and is_deleted=0 order by create_at;",
                           [user_id])
            result = cursor.fetchall()
            if len(result) > 0:
                for row in result:
                    data.append({
                        "chatbot_id": row[1],
                        "chatbot_name": row[2],
                        "chatbot_type": row[3],
                        "chatbot_persona": row[4],
                        "create_at": row[5]
                    })
            else:
                code = -1
                msg = "DetailsNotFound"

    except Exception as e:
        code = -1
        msg = str(e)
        # print(msg)

    return JsonResponse({"code": code,
                         "msg": msg,
                         "data": data})


def delete(request):
    data = request.POST
    # TODO 检查用户登陆状态
    user_id = data.get("user_id")
    chatbot_id = data.get("chatbot_id")
    code = 200
    msg = "OK"
    data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from ChatBot where user_id=%s and chatbot_id=%s and is_deleted=0;",
                           [user_id, chatbot_id])
            result = cursor.fetchall()
            if len(result) == 0:
                code = -1
                msg = "ChatbotNotFound"
            else:
                cursor.execute("update ChatBot set is_deleted=1 where user_id=%s and chatbot_id=%s;",
                               [user_id, chatbot_id])

    except Exception as e:
        code = -1
        msg = str(e)
        # print(msg)

    return JsonResponse({"code": code,
                         "msg": msg,
                         "data": data})
