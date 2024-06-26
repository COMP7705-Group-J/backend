from openai import OpenAI
from django.db import connection

import json

summarizer_prompt = "You need to summarize the import information from the following chat history between the user " \
                    "and the assistant(you). You should focus on the preference, psat experience and interesting details.\n" \
                    "You should follow the following rules in this task:\n" \
                    "1. Only extract information which are directly related to user's preference, daily events, " \
                    "habits. Avoid deeply deduct or analyze user's actions. Just briefly summarize facts.\n" \
                    " a. Preference: Topics that user explicitly like or dislike. Sensitive topics that user don't want to talk about.\n" \
                    " b. Daily Events: Events mentioned by user, such as job changes, family changes, healthy status and so on.\n" \
                    " c. Habits: User's lifestyle, preference and so on.\n" \
                    "d. Interesting details: Interesting or special details, could be an vivid expression, a unique " \
                    "   hobby or an example to show user's personality.\n" \
                    "2. You are the assistant. When you output, \"you\" represents the assistant.\n" \
                    "3. Just output an empty string if no information about user is provided.\n" \
                    "4. Briefly output the result. Don't be redundant. Directly output the result. Don't classify the result.\n" \
                    "5. Combine with the past summary between the user and the assistant, generate the complete " \
                    "summary. Don't repeat for similar or same facts. For conflicts facts, the information mentioned last time shall prevail.\n" \
                    "6. No other than explanations are need. Just output the result. Your output should begin with\"Summary: \"\n" \
                    "\n---------\n" \
                    "This is an example.\n" \
                    "chat_history:\n" \
                    "user: I ate delicious steak today.\n" \
                    "assistant: Wow, sounds nice! \n" \
                    "user: If you like, we can go for it together.\n" \
                    "assistant: sure!\n" \
                    "Summary: The user ate delicious steak and is very happy. She invite you to eat it together and you agree.\n" \
                    "\n---------\n" \
                    "Chat history between you and the user is {chat_history}\n" \
                    "Last summary beteeen you and the user is {last_summary}"

user_persona_prompt = "You need to generate the user's persona based on the provided content. Respond with only three words"

Create_User_Prompt = "You need to consider the following conversations to create the user's persona description.\
                    The conversations are between another chatbot and the user, please note that you need to create \
                    the persona for user only in short phrases and do not consider the other bot's utterance: {conversions}"

generator_prompt = "consider the history chat content and give the correspond answer." \
                   "1. If the information mentioned by the user is appeared in the summary, you should answer basing on the summary." \
                   "\n" \
                   "Summary:{last_summary}"

time_prompt = "Each user input will have a time information embedded in the front labelled by \"Time: \". If the time difference between \
            two consecutive inputs exceeds a certain threshold (e.g., 10 minutes), respond with concern or curiosity. \
            Use friendly and empathetic language. For example:\
            If the time gap is more than 10 minutes but less than 30 minutes:\
            \"I noticed it has been a little while since your last message. Is everything okay?\"\
            If the time gap is more than 30 minutes but less than an hour:\
            \"It's been a bit since we last talked. Did something come up?\"\
            If the time gap is more than an hour:\
            \"It's been a while since we last chatted. What have you been up to?\"\
            If the time gap is up to several days:\
            \"Long time no see! How do you do?\"\
            Make sure to adapt your tone to be warm and considerate, ensuring the user feels supported and not pressured."


def get_api_key():
    with open("openai_key.txt", "r", encoding="utf-8") as fin:
        return fin.readline().strip().replace("/n", "")



def get_history_chat(user_id, chatbot_id, summary):
    with connection.cursor() as cursor:
        cursor.execute(
            "select content, by_user, create_at from Chat_history where user_id = %s and chatbot_id = %s Order By create_at",
            [user_id, chatbot_id])
        row = cursor.fetchall()
    history_chat = []
    generator_prompt.format(last_summary=summary)
    history_chat.append({"role": "system", "content": generator_prompt})
    for i in range(len(row)):
        if row[i][1]:
            history_chat.append({"role": "user", "content": "Time: " + str(row[i][2]) + '\n' + row[i][0]})
        else:
            history_chat.append({"role": "assistant", "content": row[i][0]})
    return history_chat


def get_last_summary(user_id, chatbot_id):
    last_summary = ""
    with connection.cursor() as cursor:
        cursor.execute(
            "select prompt_content from Prompt where user_id = %s and chatbot_id = %s and prompt_name=%s",
            [user_id, chatbot_id, "last_summary"])
        row = cursor.fetchall()
    for i in range(len(row)):
        last_summary = row[i][0]
    return last_summary


def do_summary(user_id, chatbot_id, last_summary, chat_history):
    parsed_history = json.dumps(chat_history[1:])

    prompt = summarizer_prompt.format(chat_history=parsed_history, last_summary=last_summary)
    messages = [
        {
            "role": "system",
            "content": ""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # TODO do summary
    updated_summary = "test3"
    with connection.cursor() as cursor:
        cursor.execute("update Prompt set prompt_content=%s where user_id=%s and chatbot_id=%s and prompt_name=%s;",
                       [updated_summary, user_id, chatbot_id, "last_summary"])


def generate_user_persona(conversions):
    # TODO: 讨论一下这个函数怎么调用
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    messages = []
    messages.append({"role": "system", "content": user_persona_prompt + time_prompt})
    # messages.append({"role": "user", "content" : user_input})
    # messages.append({"role": "assistant", "content" : user_output})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=messages
    )

    return response
