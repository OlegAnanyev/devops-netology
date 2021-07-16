# Домашнее задание к занятию "14.3 Карты конфигураций"

## Задача 1: Работа с картами конфигураций через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать карту конфигураций?

```
kubectl create configmap nginx-config --from-file=nginx.conf
kubectl create configmap domain --from-literal=name=netology.ru
```

### Как просмотреть список карт конфигураций?

```
kubectl get configmaps
kubectl get configmap
```

### Как просмотреть карту конфигурации?

```
kubectl get configmap nginx-config
kubectl describe configmap domain
```

### Как получить информацию в формате YAML и/или JSON?

```
kubectl get configmap nginx-config -o yaml
kubectl get configmap domain -o json
```

### Как выгрузить карту конфигурации и сохранить его в файл?

```
kubectl get configmaps -o json > configmaps.json
kubectl get configmap nginx-config -o yaml > nginx-config.yml
```

### Как удалить карту конфигурации?

```
kubectl delete configmap nginx-config
```

### Как загрузить карту конфигурации из файла?

```
kubectl apply -f nginx-config.yml
```

![image](https://user-images.githubusercontent.com/32748936/125951907-6cddb0b3-da02-4803-8fee-e0ee51a45777.png)


## Задача 2 (*): Работа с картами конфигураций внутри модуля

Выбрать любимый образ контейнера, подключить карты конфигураций и проверить
их доступность как в виде переменных окружения, так и в виде примонтированного
тома

```
Используем конфигмап, созданный из литерала, как переменную окружения. А конфигмап, созданный из файла, примонтируем в контейнер по пути /nginx-config
```

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-backend
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
        env:
          - name: DOMAIN_FROM_CONFIGMAP
            valueFrom:
              configMapKeyRef:
                name: domain
                key: name
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config-volume
          mountPath: /nginx-config
          readOnly: true
      - name: backend
        image: olegananyev/kub-dz-backend:1
        ports:
        - containerPort: 9000
      volumes:
        - name: config-volume
          configMap:
            name: nginx-config
```

```
Применим изменённый деплоймент и, зайдя внутрь контейнера, проверим, что всё получилось:
```

![image](https://user-images.githubusercontent.com/32748936/125953588-bc177f38-62db-4255-87ea-014a6b12f6f2.png)

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, configmaps) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---
