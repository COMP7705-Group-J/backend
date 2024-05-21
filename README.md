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

## bot模块（草稿）

### bots/create - 创建机器人

* 请求方法：POST

* 请求参数：

  ```json
  {
  		"user_id":1,
  		"chatbot_name":"Bot-1",
  		"chatbot_type": 0, # 0表示普通机器人，1表示cosplay机器人。
  		"chatbot_persona": "Jackie Chan" # chatbot_type=1时传入。
  }
  ```

* 返回结果：

  ```json
  {
      "code": 200, #状态码，200为成功，-1为失败。
      "msg": "OK", #执行信息。code=200时，msg为OK。code=-1时，msg为错误信息。
      "data": [ #code=200时才有数据，code=-1时为空，可以不用管。
          {
              "chatbot_id": 15870 #如果创建机器人成功，则分配id
          }
      ]
  }
  ```

### bots/detail - 查看机器人详情

* 请求方法：POST

* 请求参数：

  ```json
  {
  		"user_id":1,
  		"chatbot_id":15870
  }
  ```

* 返回结果：

  ```json
  {
      "code": 200,
      "msg": "OK", #“DetailsNotFound”表示没找到对应ID的机器人。
      "data": [
          {
              "chatbot_name": "Bot-1",
              "chatbot_type": 1,
              "chatbot_persona": "Xiao",
              "create_at": "2024-05-22T01:19:45"
          }
      ]
  }
  ```

### bots/list - 查看机器人列表

* 请求方法：POST

* 请求参数：

  ```json
  {
  		"user_id":1
  }
  ```

* 返回结果：

  ```json
  {
      "code": 200,
      "msg": "OK",
      "data": [
          {
              "chatbot_id": 13549,
              "chatbot_name": "hahaha",
              "chatbot_type": 1,
              "chatbot_persona": "Jackie Chan",
              "create_at": "2024-05-22T00:41:04"
          },
          {
              "chatbot_id": 13601,
              "chatbot_name": "hahaha",
              "chatbot_type": 1,
              "chatbot_persona": "Jackie Chan",
              "create_at": "2024-05-22T00:41:56"
          },
          {
              "chatbot_id": 13671,
              "chatbot_name": "test1",
              "chatbot_type": 0,
              "chatbot_persona": "",
              "create_at": "2024-05-22T00:43:06"
          },
          {
              "chatbot_id": 15870,
              "chatbot_name": "Bot-1",
              "chatbot_type": 1,
              "chatbot_persona": "Xiao",
              "create_at": "2024-05-22T01:19:45"
          }
      ]
  }
  ```

### bots/delete - 删除机器人

* 请求方法：POST

* 请求参数：

  ```json
  {
  		"user_id":1,
  		"chatbot_id":"15870"
  }
  ```

* 返回结果：

  ```json
  {
      "code": 200,
      "msg": "OK", #"ChatbotNotFOund"表示要删除的机器人没找到
      "data": [] 成功时这里也为空，可以不用管。
  }
  ```

### 

