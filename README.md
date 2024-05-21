# backend

## install
pip install django\
pip install djangorestframework\
pip install pymysql\
pip install openai

## Database配置

在chatbot_backend下面创建db_config.py

```json
local_database = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '7705database',
        'USER': 'root', //改成自己的用户名
        'PASSWORD': '123456', //改成自己的密码
        'PORT': '3306', //改成自己的端口
    }
}
```



## chat 模块
URL:localhost:port/chat/history\
method:GET\
para:user_id(int),chatbot_id(int)\
response:当前用户和当前机器人聊天历史记录,json，列表(content,by_user(bool),timestamp)

URL:localhost:port/chat/new_chat\
method:GET\
para:user_id(int),chatbot_id(int),input(string? I guess)\
response:预期是ai的输出，json

## bot模块