# Домашнее задание к занятию "13.2 разделы и монтирование"
Приложение запущено и работает, но время от времени появляется необходимость передавать между бекендами данные. А сам бекенд генерирует статику для фронта. Нужно оптимизировать это.
Для настройки NFS сервера можно воспользоваться следующей инструкцией (производить под пользователем на сервере, у которого есть доступ до kubectl):
* установить helm: curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
* добавить репозиторий чартов: helm repo add stable https://charts.helm.sh/stable && helm repo update
* установить nfs-server через helm: helm install nfs-server stable/nfs-server-provisioner

В конце установки будет выдан пример создания PVC для этого сервера.

## Задание 1: подключить для тестового конфига общую папку
В stage окружении часто возникает необходимость отдавать статику бекенда сразу фронтом. Проще всего сделать это через общую папку. Требования:
* в поде подключена общая папка между контейнерами (например, /static);
* после записи чего-либо в контейнере с беком файлы можно получить из контейнера с фронтом.

```
Добавим в деплоймент volume с именем static и примонтируем его к обоим контенейрам в поде:
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
        ports:
        - containerPort: 80
        volumeMounts:
        - mountPath: /static
          name: static

      - name: backend
        image: olegananyev/kub-dz-backend:1
        ports:
        - containerPort: 9000
        volumeMounts:
        - mountPath: /static
          name: static
                  
      volumes:
      - name: static
        emptyDir: {}
```

```
Проверим:
```

```bash
root@node1:/home/hawk# k get pods
NAME                                  READY   STATUS    RESTARTS   AGE
db-0                                  1/1     Running   0          7m31s
frontend-backend-66ccf6bb79-lf8hz     2/2     Running   0          2m59s
nfs-server-nfs-server-provisioner-0   1/1     Running   0          12m
root@node1:/home/hawk# k exec -it frontend-backend-66ccf6bb79-lf8hz -c frontend /bin/bash
root@frontend-backend-66ccf6bb79-lf8hz:/app# cd /static
root@frontend-backend-66ccf6bb79-lf8hz:/static# touch hello-from-frontend
root@frontend-backend-66ccf6bb79-lf8hz:/static# exit
root@node1:/home/hawk# k exec -it frontend-backend-66ccf6bb79-lf8hz -c backend /bin/bash
root@frontend-backend-66ccf6bb79-lf8hz:/app# cd /static
root@frontend-backend-66ccf6bb79-lf8hz:/static# ls
hello-from-frontend
```

## Задание 2: подключить общую папку для прода
Поработав на stage, доработки нужно отправить на прод. В продуктиве у нас контейнеры крутятся в разных подах, поэтому потребуется PV и связь через PVC. Сам PV должен быть связан с NFS сервером. Требования:
* все бекенды подключаются к одному PV в режиме ReadWriteMany;
* фронтенды тоже подключаются к этому же PV с таким же режимом;
* файлы, созданные бекендом, должны быть доступны фронту.
