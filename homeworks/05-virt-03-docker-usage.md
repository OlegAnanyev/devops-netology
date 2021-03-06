# Домашнее задание к занятию "5.3. Контейнеризация на примере Docker"

## Задача 1 

"Подходит ли в этом сценарии использование докера? Или лучше подойдет виртуальная машина, физическая машина? Или возможны разные варианты?"

- Высконагруженное монолитное java веб-приложение;
`Лучше использовать физический сервер или виртуальную машину, т.к. Докер плохо подходит для высоконагруженных монолитных приложений.`

- Go-микросервис для генерации отчетов;
`Docker будет хорошим вариантом.`

- Nodejs веб-приложение;
`Зависит от архитектуры приложения, но в общем случае, если нет экстремальных требований по производительности, Докер будет хорошим выбором.`

- Мобильное приложение c версиями для Android и iOS;
`Докер не подходит для мобильных приложений и в целом для приложений с графическим интерфейсом.`

- База данных postgresql используемая, как кэш;
`Полагаю, что Докер будет удобен в данном случае.`

- Шина данных на базе Apache Kafka;
`Не знаком глубоко с Apache Kafka, но судя по найденной информации, такие системы успешно запускают в среде Докер.`

- Очередь для Logstash на базе Redis;
`Докер вполне подойдёт.`

- Elastic stack для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
`Докер в связке с Kubernetes будет хорошим решением для управления такой инфраструктурой.`

- Мониторинг-стек на базе prometheus и grafana;
`Также можно использовать Докер.`

- Mongodb, как основное хранилище данных для java-приложения;
`Думаю, что в данном случае стоит использовать физический или виртуальный сервер, т.к. Докер только снизит производительность и добавит сложностей с управлением БД.`

- Jenkins-сервер.
`Опять же, Докер будет хорошим решением.`

## Задача 2 

[https://hub.docker.com/r/olegananyev/netology-httpd](https://hub.docker.com/r/olegananyev/netology-httpd)

## Задача 3 

![screenshot](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/05-virt-03-docker-usage.png)
