
# Домашнее задание к занятию "11.02 Микросервисы: принципы"

Вы работаете в крупной компанию, которая строит систему на основе микросервисной архитектуры.
Вам как DevOps специалисту необходимо обеспечить настройку систем для обеспечения работы системы.


## Задача 1: API Gateway

### Есть три сервиса:

**minio**
- Хранит загруженные файлы в бакете images
- S3 протокол

**uploader**
- Принимает файл, если он картинка сжимает и загружает его в minio
- POST /v1/upload

**security**
- Регистрация пользователя POST /v1/user
- Получение информации о пользователе GET /v1/user
- Логин пользователя POST /v1/token
- Проверка токена GET /v1/token/validation

### Необходимо воспользоваться любым балансировщиком и сделать API Gateway:

**POST /v1/register**
- Анонимный доступ.
- Запрос направляется в сервис security POST /v1/user

**POST /v1/token**
- Анонимный доступ.
- Запрос направляется в сервис security POST /v1/token

**GET /v1/user**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис security GET /v1/user

**POST /v1/upload**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис uploader POST /v1/upload

**GET /v1/user/{image}**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис minio  GET /images/{image}

### Ожидаемый результат

Результатом выполнения задачи должен быть docker compose файл запустив который можно локально выполнить следующие команды с успешным результатом.
Предполагается что для реализации API Gateway будет написан конфиг для NGinx или другого балансировщика нагрузки который будет запущен как сервис через docker-compose и будет обеспечивать балансировку и проверку аутентификации входящих запросов.
Авторизаци
curl -X POST -H 'Content-Type: application/json' -d '{"login":"bob", "password":"qwe123"}' http://localhost/token

**Загрузка файла**

curl -X POST -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJib2IifQ.hiMVLmssoTsy1MqbmIoviDeFPvo-nCd92d4UFiN2O2I' -H 'Content-Type: octet/stream' --data-binary @yourfilename.jpg http://localhost/upload

**Получение файла**
curl -X GET http://localhost/images/4e6df220-295e-4231-82bc-45e4b1484430.jpg

# РЕШЕНИЕ
Для решения поставленной в ДЗ задачи потребовалось только создать конфигурацию nginx.
Полный docker-compose: https://github.com/OlegAnanyev/devops-netology/tree/master/homeworks/11-microservices-02-principles

nginx.conf:
```
events {
    worker_connections 1024;
    multi_accept on;
}

http {
    server {
        listen 8080;

        location /register {
            proxy_pass http://security:3000/v1/user;
        }
        location /token {
            proxy_pass http://security:3000/v1/token;
        }

        location /user {
            auth_request /auth;            
            proxy_pass http://security:3000/v1/user;
        }

        location /upload {
            auth_request /auth;
            proxy_pass http://uploader:3000/v1/upload;
        }   

        location /images/ {
            proxy_pass http://storage:9000/data/;
        }

        location /auth {
            internal;
            proxy_pass              http://security:3000/v1/token/validation;
            proxy_pass_request_body off;
            proxy_set_header        Content-Length "";
            proxy_set_header        X-Original-URI $request_uri;
        }               
    }
}
```

## Проверяем
```bash
#пытаемся загрузить файл без авторизации
05:37:16 $ curl -X POST -H 'Content-Type: octet/stream' --data-binary @1.jpg http://localhost/upload
<html>
<head><title>401 Authorization Required</title></head>
<body>
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx</center>
</body>
</html>

#получаем токен для авторизации
05:37:40 $ curl -X POST -H 'Content-Type: application/json' -d '{"login":"bob", "password":"qwe123"}' http://localhost/token
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJib2IifQ.hiMVLmssoTsy1MqbmIoviDeFPvo-nCd92d4UFiN2O2I

#загружаем файл с авторизацией
05:38:03 $ curl -X POST -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJib2IifQ.hiMVLmssoTsy1MqbmIoviDeFPvo-nCd92d4UFiN2O2I' -H 'Content-Type: octet/stream' --data-binary @1.jpg http://localhost/upload
{"filename":"edf205f7-bbf4-4ceb-934f-70bac9323acb.jpg"}

#скачиваем файл (curl предупреждает, что терминал сломается от вывода бинарного файла, но можем всё-таки рискнуть, добавив в конце  --output -)

05:39:15 $ curl http://localhost/images/edf205f7-bbf4-4ceb-934f-70bac9323acb.jpg > edf205f7-bbf4-4ceb-934f-70bac9323acb.jpg
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1818  100  1818    0     0   355k      0 --:--:-- --:--:-- --:--:--  355k
```
