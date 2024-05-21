# User Module

## requirements
```shell
pip install djangorestframework-simplejwt
pip install django-filter
pip install drf-extensions
```

## Apis
### login/
* method
`POST`
* request body
username/email and passwords in string types
```shell
{"username": "<can be either a username or a email>", "password": "..."}
```
* response body
refresh and access tokens in string types if success
```shell
{"refresh": "...", "access": "..."}
```
or if the username/password is wrong:
```shell
{"detail": "No active account found with the given credentials"}
```
### register/
* method
`POST`
* request body
username, passwords and email(optional) in string types
```shell
{"username": "...", "password": "...", ["email": "..."]}
```
* response body
```shell
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
```shell
{"username": ["A user with that username already exists."]}
```
### users/users/\<id\>/
* method
`GET`
this is a test for the token login, there are some issues to be fixed at present




