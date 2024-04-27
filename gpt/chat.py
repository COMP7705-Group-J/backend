import openai
from openai import OpenAI
from pathlib import Path



def add_persona_if_exist(prefix, file_name):
    persona_file_path = "./persona_{}".format(file_name)
    if Path(persona_file_path).exists():
        with open(persona_file_path, "r") as fin:
            persona = fin.readline().strip().replace("/n", "")
            persona_prompt = " Three words to describe the user you are talking to is {}." \
                             "You should also consider these descriptions when giving responses.".format(persona)
        return prefix + persona_prompt
    else:
        return prefix


def parse_history_talk(file_name):
    history_talk = []
    with open(file_name, "r", encoding="utf-8") as fin:
        system = fin.readline().strip().replace("/n", "").split(": ")
        history_talk.append({"role": "system", "content": add_persona_if_exist(system[1], file_name)})
        for line in fin.readlines():
            tmp = line.strip().split(": ")
            role = tmp[0]
            content = tmp[1]
            history_talk.append({"role": role, "content": content})
    return history_talk


def append_file(file_name, user, assistant):
    with open(file_name, "a") as fout:
        fout.write("user: {}\n".format(user))
        fout.write("assistant: {}\n".format(assistant))


def get_api_key():
    with open("openai_key.txt", "r", encoding="utf-8") as fin:
        return fin.readline().strip().replace("/n", "")


def test_daily_chat(client, file_name):
    history_chat = parse_history_talk(file_name)
    user_input = input("USER: ")
    history_chat.append({"role": "user", "content": user_input})
    response = daily_chat(client, history_chat)
    print(history_chat)
    print("ASSISTANT: {}".format(response))
    append_file(file_name, user_input, response)


def test_customized_chat(client, file_name):
    test_daily_chat(client, file_name)


def daily_chat(client, history_chat):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        seed=1,
        messages=history_chat
    )
    if response.choices[0].finish_reason != "stop":
        # monitor
        pass
    print("============================================================")
    print("prompt_tokens {}, completion_tokens {}, total_tokens {}".format(response.usage.prompt_tokens,
                                                                           response.usage.completion_tokens,
                                                                           response.usage.total_tokens))
    print("============================================================")
    return response.choices[0].message.content


def test_generate_persona(client, file_name):
    prompt = []
    system_content = "You will be provided with a conversation between a user and an assistant. " \
                     "The conversation is delimited with XML tags. " \
                     "Please to give me three words split with commas, to conclude the persona of the user. " \
                     "Don't answer if you have not come up with three words."
    prompt.append({"role": "system", "content": system_content})
    with open(file_name, "r", encoding="utf-8") as fin:
        fin.readline()
        prompt.append({"role": "user", "content": "<p>{}</p>".format(fin.read())})

    response = daily_chat(client, prompt)
    print("ASSISTANT: {}".format(response))

    with open("persona_{}".format(file_name), "w") as fout:
        fout.write(response.lower())


if __name__ == '__main__':
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    # test_daily_chat(client, "daily_chat.txt")
    # test_customized_chat(client, "customized_chat_JackieChan.txt")

    test_generate_persona(client, "daily_chat.txt")

