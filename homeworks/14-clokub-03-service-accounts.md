# Домашнее задание к занятию "14.4 Сервис-аккаунты"

## Задача 1: Работа с сервис-аккаунтами через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать сервис-аккаунт?

```
kubectl create serviceaccount netology
```

```
[hawk:~] $ kubectl create serviceaccount netologydz
serviceaccount/netologydz created
```

### Как просмотреть список сервис-акаунтов?

```
kubectl get serviceaccounts
kubectl get serviceaccount
```

```
[hawk:~] $ kubectl get serviceaccounts
NAME               SECRETS   AGE
default            1         10d
netologydz         1         1d
```
### Как получить информацию в формате YAML и/или JSON?

```
kubectl get serviceaccount netology -o yaml
kubectl get serviceaccount default -o json
```

```
[hawk:~] $ kubectl get serviceaccount netologydz -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2021-08-08T14:21:02Z"
  name: netologydz
  namespace: default
  resourceVersion: "779349"
  uid: c5a2b3ba-f91f-11eb-9a03-0242ac130003
secrets:
- name: netology-token-ndjrh
[hawk:~] $ kubectl get serviceaccount netologydz -o json
{
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "creationTimestamp": "2021-08-08T14:21:02Z",
        "name": "default",
        "namespace": "default",
        "resourceVersion": "431",
        "uid": "c5a2b3ba-f91f-11eb-9a03-0242ac130003"
    },
    "secrets": [
        {
            "name": "default-token-ndjrh"
        }
    ]
}
```
### Как выгрузить сервис-акаунты и сохранить его в файл?

```
kubectl get serviceaccounts -o json > serviceaccounts.json
kubectl get serviceaccount netology -o yaml > netology.yml
```

```
[hawk:~] $ kubectl get serviceaccount netologydz -o yaml > netologydz.yml
```
### Как удалить сервис-акаунт?

```
kubectl delete serviceaccount netology
```

```
[hawk:~] $ kubectl delete serviceaccount netologydz
serviceaccount "netologydz" deleted
```
### Как загрузить сервис-акаунт из файла?

```
kubectl apply -f netology.yml
```

```
[hawk:~] $ kubectl apply -f netologydz.yml
serviceaccount/netologydz created
```
## Задача 2 (*): Работа с сервис-акаунтами внутри модуля

Выбрать любимый образ контейнера, подключить сервис-акаунты и проверить
доступность API Kubernetes

```
kubectl run -i --tty fedora --image=fedora --restart=Never -- sh
```

Просмотреть переменные среды

```
env | grep KUBE
```

Получить значения переменных

```
K8S=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT
SADIR=/var/run/secrets/kubernetes.io/serviceaccount
TOKEN=$(cat $SADIR/token)
CACERT=$SADIR/ca.crt
NAMESPACE=$(cat $SADIR/namespace)
```

Подключаемся к API

```
curl -H "Authorization: Bearer $TOKEN" --cacert $CACERT $K8S/api/v1/
```

В случае с minikube может быть другой адрес и порт, который можно взять здесь

```
cat ~/.kube/config
```

или здесь

```
kubectl cluster-info
```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, serviceaccounts) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---
