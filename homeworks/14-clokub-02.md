# Домашнее задание к занятию "14.2 Синхронизация секретов с внешними сервисами. Vault"

## Задача 1: Работа с модулем Vault

Запустить модуль Vault конфигураций через утилиту kubectl в установленном minikube

```
kubectl apply -f 14.2/vault-pod.yml
```

Получить значение внутреннего IP пода

```
kubectl get pod 14.2-netology-vault -o json | jq -c '.status.podIPs'
```

Примечание: jq - утилита для работы с JSON в командной строке

Запустить второй модуль для использования в качестве клиента

```
kubectl run -i --tty fedora --image=fedora --restart=Never -- sh
```

Установить дополнительные пакеты

```
dnf -y install pip
pip install hvac
```

Запустить интепретатор Python и выполнить следующий код, предварительно
поменяв IP и токен

```
import hvac
client = hvac.Client(
    url='http://10.10.133.71:8200',
    token='aiphohTaa0eeHei'
)
client.is_authenticated()

# Пишем секрет
client.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(netology='Big secret!!!'),
)

# Читаем секрет
client.secrets.kv.v2.read_secret_version(
    path='hvac',
)
```


Решение

Мой конфиг Vault:
```yml
---
apiVersion: v1
kind: Pod
metadata:
  name: 14.2-netology-vault
spec:
  containers:
  - name: vault
    image: vault
    ports:
    - containerPort: 8200
      protocol: TCP
    env:
    - name: VAULT_DEV_ROOT_TOKEN_ID
      value: "ololotoken"
    - name: VAULT_DEV_LISTEN_ADDRESS
      value: 0.0.0.0:8200

```

Мой скрипт для проверки работоспособности:
```python
import hvac
client = hvac.Client(
    url='http://10.233.96.151:8200',
    token='ololotoken'
)
client.is_authenticated()

# Пишем секрет
client.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(netology='Big secret!!!'),
)

# Читаем секрет
client.secrets.kv.v2.read_secret_version(
    path='hvac',
)
```
![image](https://user-images.githubusercontent.com/32748936/125627063-c85f1433-4c35-4809-8657-00967831f4c4.png)



## Задача 2 (*): Работа с картами конфигураций внутри модуля

* На основе образа fedora создать модуль;
* Создать секрет, в котором будет указан токен;
* Подключить секрет к модулю;
* Запустить модуль и проверить доступность сервиса Vault.


Изменим в конфиге Vault токен на "ololotoken_from_secret", при этом у меня ip сменился на 10.233.96.161.

Конфиг тестового пода (вместо Fedora я решил использовать контейнер python, т.к. в нём уже есть pip):
```yml
apiVersion: v1
kind: Pod
metadata:
  name: python-test-vault
spec:
  containers:
  - name: python-test-vault
    image: python
    env:
      - name: VAULT_TOKEN
        valueFrom:
          secretKeyRef:
            name: vault-token
            key: token
  restartPolicy: Never
```

Создадим секрет со значением токена:
```bash
root@node1:/home/hawk# kubectl create secret generic vault-token --from-literal=token=ololotoken_from_secret
secret/vault-token created
```

Скрипт для тестирования:
```
import hvac
import os
client = hvac.Client(
    url='http://10.233.96.161:8200',
    token=os.environ['VAULT_TOKEN']
)
client.is_authenticated()

# Пишем секрет
client.secrets.kv.v2.create_or_update_secret(
    path='hvac',
    secret=dict(netology='Big secret with secret token!!!'),
)

# Читаем секрет
client.secrets.kv.v2.read_secret_version(
    path='hvac',
)
```

Логинимся в консоль тестового контейнера:
![image](https://user-images.githubusercontent.com/32748936/125636203-2f833dd0-e94e-4c46-bdbe-a4dc239251ed.png)

Проверяем, что токен для Vault доступен через переменную окружения и всё работает:
![image](https://user-images.githubusercontent.com/32748936/125640619-8776b4ea-c82b-45a1-8162-2ce7036ff79e.png)





---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, statefulset, service) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---
