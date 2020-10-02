# Домашнее задание к занятию "5.3. Контейнеризация на примере Docker"

## Задача 1 

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование докера? Или лучше подойдет виртуальная машина, физическая машина? Или возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высконагруженное монолитное java веб-приложение; 
- Go-микросервис для генерации отчетов;
- Nodejs веб-приложение;
- Мобильное приложение c версиями для Android и iOS;
- База данных postgresql используемая, как кэш;
- Шина данных на базе Apache Kafka;
- Очередь для Logstash на базе Redis;
- Elastic stack для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
- Мониторинг-стек на базе prometheus и grafana;
- Mongodb, как основное хранилище данных для java-приложения;
- Jenkins-сервер.

## Задача 2 

[https://hub.docker.com/r/olegananyev/netology-httpd](https://hub.docker.com/r/olegananyev/netology-httpd)

## Задача 3 

![screenshot](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/05-virt-03-docker-usage.png)