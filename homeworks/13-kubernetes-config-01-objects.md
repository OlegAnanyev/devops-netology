# Домашнее задание к занятию "13.1 контейнеры, поды, deployment, statefulset, services, endpoints"
Настроив кластер, подготовьте приложение к запуску в нём. Приложение стандартное: бекенд, фронтенд, база данных (пример можно найти в папке 13-kubernetes-config).

## Задание 1: подготовить тестовый конфиг для запуска приложения
Для начала следует подготовить запуск приложения в stage окружении с простыми настройками. Требования:
* под содержит в себе 3 контейнера — фронтенд, бекенд, базу;
* регулируется с помощью deployment фронтенд и бекенд;
* база данных — через statefulset.

```
По сути задания получается, что всё-таки не один под с 3 контейнерами, а 2+1, т.к. контейнер БД должен быть в своём поде в рамках statefulset-а.
Ниже конфиг:
```

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dz-deployment
  labels:
    app: dz
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dz
  template:
    metadata:
      labels:
        app: dz
    spec:
      containers:
      - name: frontend
        image: olegananyev/kub-dz-frontend:1
        ports:
        - containerPort: 80
      - name: backend
        image: olegananyev/kub-dz-backend:1
        ports:
        - containerPort: 9000
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  selector:
    matchLabels:
      app: db
  serviceName: "db"
  replicas: 1
  template:
    metadata:
      labels:
        app: db
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: db
        image: postgres:13-alpine
        ports:
        - containerPort: 5432
        env:
          - name: POSTGRES_PASSWORD
            value: postgres
          - name: POSTGRES_USER
            value: postgres
          - name: POSTGRES_DB
            value: news
```

## Задание 2: подготовить конфиг для production окружения
Следующим шагом будет запуск приложения в production окружении. Требования сложнее:
* каждый компонент (база, бекенд, фронтенд) запускаются в своем поде, регулируются отдельными deployment’ами;
* для связи используются service (у каждого компонента свой);
* в окружении фронта прописан адрес сервиса бекенда;
* в окружении бекенда прописан адрес сервиса базы данных.

## Задание 3 (*): добавить endpoint на внешний ресурс api
Приложению потребовалось внешнее api, и для его использования лучше добавить endpoint в кластер, направленный на это api. Требования:
* добавлен endpoint до внешнего api (например, геокодер).

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, statefulset, service) или скриншот из самого Kubernetes, что сервисы подняты и работают.

---
