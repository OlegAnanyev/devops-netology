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
Добавим в деплоймент volume с именем static и
примонтируем его к обоим контенейрам в поде:
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

```
Для нормальной работы NFS-провиженера потребовалось сделать
"apt-get install -y nfs-common" на всех нодах кластера,
без этого не работало (что в принципе логично).
Применим конфигурацию с pv и проверим доступность
volume из разных подов.
```

```bash
root@node1:/home/hawk# k apply -f prod.yml
deployment.apps/frontend created
deployment.apps/backend created
statefulset.apps/db created
service/frontend created
service/backend created
service/db created
persistentvolumeclaim/static-pvc created
root@node1:/home/hawk# k get pods
NAME                                  READY   STATUS    RESTARTS   AGE
backend-bdbd584cf-fwvfz               1/1     Running   0          9s
db-0                                  1/1     Running   0          9s
frontend-6576f7dd68-84hgs             1/1     Running   0          9s
nfs-server-nfs-server-provisioner-0   1/1     Running   0          15m
root@node1:/home/hawk# k exec -it backend-bdbd584cf-fwvfz /bin/bash
root@backend-bdbd584cf-fwvfz:/app# touch /static/hello-from-backend
root@backend-bdbd584cf-fwvfz:/app# exit
root@node1:/home/hawk# k exec -it frontend-6576f7dd68-84hgs /bin/bash
root@frontend-6576f7dd68-84hgs:/app# ls /static
hello-from-backend

```

Полный конфиг:
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: olegananyev/kub-dz-frontend:1
        ports:
        - containerPort: 80
        env:
          - name: BASE_URL
            value: http://backend:9000
        volumeMounts:
        - mountPath: /static
          name: static-pv

      volumes:
      - name: static-pv
        persistentVolumeClaim:
          claimName: static-pvc
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: olegananyev/kub-dz-backend:1
        ports:
        - containerPort: 9000
        env:
          - name: DATABASE_URL
            value: postgres://postgres:postgres@db:5432/news
        volumeMounts:
        - mountPath: /static
          name: static-pv

      volumes:
      - name: static-pv
        persistentVolumeClaim:
          claimName: static-pvc
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
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 9000
      targetPort: 9000
---
apiVersion: v1
kind: Service
metadata:
  name: db
spec:
  selector:
    app: db
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432

---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: static-pvc
spec:
  storageClassName: "nfs"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Mi
```
