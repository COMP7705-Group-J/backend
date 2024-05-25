# backend

## install
pip install django\
pip install djangorestframework\
pip install pymysql\
pip install openai\
pip install djangorestframework-simplejwt\
pip install django-filter\
pip install drf-extensions\

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
### 历史记录
* URL: localhost:port/chat/history
* method: GET
* parameter: 
  ```json
  {
  		"user_id": 1,
  		"chatbot_id": 1,
  }
  ```
* response: 
    ```json
  {
      "code": 200,
      "msg": "ok",
  		"data":[
            [
                "content":"...",
                "by_user": 1, # bool
                "timestamp": "2024-05-21T15:53:25"
            ],
            [
                "content":"...",
                "by_user": 0,
                "timestamp": "2024-05-21T15:53:25"
            ],
            ...
        ]
  }
  ```

### chat list
* URL: localhost:port/chat/list
* method: GET
* parameter: 
  ```json
  {
  		"user_id": 1,
  }
  ```
* response: 
    ```json
  {
      "code": 200,
      "msg": "ok",
      "data": [
            [
              "chatbot_id": 2, 
              "timestamp": "2024-05-23T16:44:55", 
              "content": "test data3" #这里会返回最新的来自每个bot的输出
            ], 
            [
              "chatbot_id": 1,
              "timestamp": "2024-05-23T16:44:53",
              "content": "test data1"
            ],
            ...
          ]
  }
  ```


### 发送当前聊天内容至机器人
* URL: localhost:port/chat/new_chat
* method: POST
* parameter:
  ```json
  {
  		"user_id": 1,
  		"chatbot_id": 1,
  		"input": "replace with user input"
  }
  ```
* response:
  ```json
  {
      "code": 200,#暂定，未处理openai的api中可能的错误
      "msg": "ok",
  		"data": "replace with openai output"
  }
  ```


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

## User模块

### login/ - 用户登录
* method
`POST`
* request body

username/email and passwords in string types
```json
{"username": "<can be either a username or an email>", "password": "..."}
```
* response body

refresh and access tokens in string types if success
```json
{"refresh": "...", "access": "..."}
```
or if the username/password is wrong:
```json
{"detail": "No active account found with the given credentials"}
```
### users/register/  - 用户注册
* method
`POST`
* request body

username, passwords and email(optional) in string types
```json
{"username": "...", "password": "...", ["email": "..."]}
```
* response body
```json
{
    "code": 201,
    "msg": "OK",
    "data": {
        "username": "...",
        "password": "...",
        "email": "..."
    }
}
```
or if the username already exists:
```json
{"username": ["A user with that username already exists."]}
```
### users/users/\<id\>/ - 更改第\<id\>个用户的信息(待重写)
* method
`PATCH`
* request header plus:
```shell
key = Authorization
value = "Bearer" + " " + access_token   #access token from the return of login/
```
* request body:
```json
{
    "username": "...",
    "password": "...",
    "email": "..."
}
```
* response body
```json
{
    "code": 200,
    "msg": "OK",
    "data": {
        "username": "...",
        "email": "..."
    }
}
```
or if the token is invalid or expired:
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

this is a test for the token login, there are some issues to be fixed at present

