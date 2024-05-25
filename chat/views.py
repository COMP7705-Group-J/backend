from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import connection
import openai
# Create your views here.

def get_api_key():
    with open("openai_key.txt", "r", encoding="utf-8") as fin:
        return fin.readline().strip().replace("/n", "")

def list_chat(request):
    user_id = request.GET.get("user_id")
    with connection.cursor() as cursor:
        cursor.execute("SELECT chatbot_id, create_at, content\
                        FROM (\
                            SELECT chatbot_id, create_at, content, ROW_NUMBER() OVER (PARTITION BY chatbot_id ORDER BY create_at DESC) AS rn\
                            FROM Chat_history WHERE user_id = %s\
                            ) AS subquery\
                        WHERE rn = 1 ORDER BY create_at DESC", [user_id])
        row = cursor.fetchall()
    return JsonResponse({"data":row})

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
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 1);", [user_id,chatbot_id,input])
    # todo:丢到模型里产生输出
    output = "replace with openai output"

    openai.api_key = get_api_key()

    prompt = "User: {}\nChatGPT: ".format(input)

    response = openai.Completion.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=prompt
    )

    output = response.choices[0].text.strip()

    with connection.cursor() as cursor:
        cursor.execute("insert into Chat_history values (%s,%s,NOW(),%s, 0);", [user_id, chatbot_id, output])

    return JsonResponse({"data": output})