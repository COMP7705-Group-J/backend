from openai import OpenAI

summarizer_prompt = "You need to summarize the current conversation about another chatbot and the user, summarize the event"

user_persona_prompt = "You need to generate the user's persona based on the provided content. Respond with only three words"

Create_User_Prompt = "You need to consider the following conversations to create the user's persona description.\
                    The conversations are between another chatbot and the user, please note that you need to create \
                    the persona for user only in short phrases and do not consider the other bot's utterance: {conversions}"

def get_api_key():
    with open("openai_key.txt", "r", encoding="utf-8") as fin:
        return fin.readline().strip().replace("/n", "")

def summary(user_input, user_output):
    # 这个函数在generator产生回复之后调用，总结当前对话
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    messages = []
    messages.append({"role": "system", "content" : summarizer_prompt})
    messages.append({"role": "user", "content" : user_input})
    messages.append({"role": "assistant", "content" : user_output})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=messages
    )

    return response

def generate_user_persona(conversions):
    # TODO: 讨论一下这个函数怎么调用
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    messages = []
    messages.append({"role": "system", "content" : user_persona_prompt})
    # messages.append({"role": "user", "content" : user_input})
    # messages.append({"role": "assistant", "content" : user_output})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=messages
    )

    return response