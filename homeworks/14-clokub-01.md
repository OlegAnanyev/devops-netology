# Домашнее задание к занятию "14.1 Создание и использование секретов"

## Задача 1: Работа с секретами через утилиту kubectl в установленном minikube

Выполните приведённые ниже команды в консоли, получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать секрет?

```
openssl genrsa -out cert.key 4096
openssl req -x509 -new -key cert.key -days 3650 -out cert.crt \
-subj '/C=RU/ST=Moscow/L=Moscow/CN=server.local'
kubectl create secret tls domain-cert --cert=certs/cert.crt --key=certs/cert.key
```

### Как просмотреть список секретов?

```
kubectl get secrets
kubectl get secret
```

### Как просмотреть секрет?

```
kubectl get secret domain-cert
kubectl describe secret domain-cert
```

### Как получить информацию в формате YAML и/или JSON?

```
kubectl get secret domain-cert -o yaml
kubectl get secret domain-cert -o json
```

### Как выгрузить секрет и сохранить его в файл?

```
kubectl get secrets -o json > secrets.json
kubectl get secret domain-cert -o yaml > domain-cert.yml
```

### Как удалить секрет?

```
kubectl delete secret domain-cert
```

### Как загрузить секрет из файла?

```
kubectl apply -f domain-cert.yml
```

Итого:
```bash
#сгнерируем сертификат и создадим из него секрет
root@node1:~/14-1# openssl genrsa -out cert.key 4096
openssl req -x509 -new -key cert.key -days 3650 -out cert.crt \
-subj '/C=RU/ST=Moscow/L=Moscow/CN=server.local'
kubectl create secret tls domain-cert --cert=cert.crt --key=cert.key
Generating RSA private key, 4096 bit long modulus (2 primes)
........................................................................++++
....++++
e is 65537 (0x010001)
secret/domain-cert created

# посмотрим список секретов
root@node1:~/14-1# kubectl get secrets
NAME                                            TYPE                                  DATA   AGE
default-token-cgml5                             kubernetes.io/service-account-token   3      45d
domain-cert                                     kubernetes.io/tls                     2      11s
nfs-server-nfs-server-provisioner-token-rbh7f   kubernetes.io/service-account-token   3      11d
sh.helm.release.v1.nfs-server.v1                helm.sh/release.v1                    1      11d

# получим краткое описание секрета domain-cert
root@node1:~/14-1# kubectl get secret domain-cert
NAME          TYPE                DATA   AGE
domain-cert   kubernetes.io/tls   2      69s

# получим подробное описание секрета domain-cert
root@node1:~/14-1# kubectl describe secret domain-cert
Name:         domain-cert
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  kubernetes.io/tls

Data
====
tls.crt:  1944 bytes
tls.key:  3243 bytes

# получим секрет в формате YML
root@node1:~/14-1# kubectl get secret domain-cert -o yaml
apiVersion: v1
data:
  tls.crt: LS0tLS1CRU...S0tLS0K
  tls.key: LS0tLS1CRUdJTi...S0tLS0K
kind: Secret
metadata:
  creationTimestamp: "2021-07-12T12:57:04Z"
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:data:
        .: {}
        f:tls.crt: {}
        f:tls.key: {}
      f:type: {}
    manager: kubectl-create
    operation: Update
    time: "2021-07-12T12:57:04Z"
  name: domain-cert
  namespace: default
  resourceVersion: "5040999"
  uid: 295db217-76d0-49ff-a67d-ddbb6f6995ef
type: kubernetes.io/tls

# получим секрет в формате json
root@node1:~/14-1# kubectl get secret domain-cert -o json
{
    "apiVersion": "v1",
    "data": {
        "tls.crt": "LS0tLS1CRUdJT...S0tLS0K",
        "tls.key": "LS0tLS1...0tLS0K"
    },
    "kind": "Secret",
    "metadata": {
        "creationTimestamp": "2021-07-12T12:57:04Z",
        "managedFields": [
            {
                "apiVersion": "v1",
                "fieldsType": "FieldsV1",
                "fieldsV1": {
                    "f:data": {
                        ".": {},
                        "f:tls.crt": {},
                        "f:tls.key": {}
                    },
                    "f:type": {}
                },
                "manager": "kubectl-create",
                "operation": "Update",
                "time": "2021-07-12T12:57:04Z"
            }
        ],
        "name": "domain-cert",
        "namespace": "default",
        "resourceVersion": "5040999",
        "uid": "295db217-76d0-49ff-a67d-ddbb6f6995ef"
    },
    "type": "kubernetes.io/tls"
}

# выгрузим секрет в JSON
root@node1:~/14-1# kubectl get secrets -o json > secrets.json
# и в YML
root@node1:~/14-1# kubectl get secret domain-cert -o yaml > domain-cert.yml
# убедимся, что секрет в обоих форматах выгрузился
root@node1:~/14-1# ll
total 64
drwxr-xr-x  2 root root  4096 Jul 12 12:59 ./
drwx------ 12 root root  4096 Jul 12 12:51 ../
-rw-r--r--  1 root root  1944 Jul 12 12:57 cert.crt
-rw-------  1 root root  3243 Jul 12 12:57 cert.key
-rw-r--r--  1 root root  7413 Jul 12 12:59 domain-cert.yml
-rw-r--r--  1 root root 40389 Jul 12 12:59 secrets.json
# удалим секрет
root@node1:~/14-1# kubectl delete secret domain-cert
secret "domain-cert" deleted
# создаим секрет из выгруженного ранее конфига
root@node1:~/14-1# kubectl apply -f domain-cert.yml
secret/domain-cert created
```

## Задача 2 (*): Работа с секретами внутри модуля

Выберите любимый образ контейнера, подключите секреты и проверьте их доступность
как в виде переменных окружения, так и в виде примонтированного тома.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (deployments, pods, secrets) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---
