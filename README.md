# backend

## chat 模块
URL:localhost:<port>/chat/history
method:GET
para:user_id(int),chatbot_id(int)
response:当前用户和当前机器人聊天历史记录,json，列表(content,by_user(bool),timestamp)

URL:localhost:<port>/chat/new_chat
method:GET
para:user_id(int),chatbot_id(int),input(string? I guess)
response:预期是ai的输出，json