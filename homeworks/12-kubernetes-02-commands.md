# Домашнее задание к занятию "12.2 Команды для работы с Kubernetes"
Кластер — это сложная система, с которой крайне редко работает один человек. Квалифицированный devops умеет наладить работу всей команды, занимающейся каким-либо сервисом.
После знакомства с кластером вас попросили выдать доступ нескольким разработчикам. Помимо этого требуется служебный аккаунт для просмотра логов.

## Задание 1: Запуск пода из образа в деплойменте
Для начала следует разобраться с прямым запуском приложений из консоли. Такой подход поможет быстро развернуть инструменты отладки в кластере. Требуется запустить деплоймент на основе образа из hello world уже через deployment. Сразу стоит запустить 2 копии приложения (replicas=2). 

Требования:
 * пример из hello world запущен в качестве deployment
 * количество реплик в deployment установлено в 2
 * наличие deployment можно проверить командой kubectl get deployment
 * наличие подов можно проверить командой kubectl get pods

```
root@ubuntu-server:~# kubectl scale --replicas=2 deployment/hello-node

root@ubuntu-server:~# kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   2/2     2            2           2d4h
root@ubuntu-server:~# kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-7567d9fdc9-xgglb   1/1     Running   0          2d4h
hello-node-7567d9fdc9-xs5nm   1/1     Running   0          2d4h
```

## Задание 2: Просмотр логов для разработки
Разработчикам крайне важно получать обратную связь от штатно работающего приложения и, еще важнее, об ошибках в его работе. 
Требуется создать пользователя и выдать ему доступ на чтение конфигурации и логов подов в app-namespace.

Требования: 
 * создан новый токен доступа для пользователя
 * пользователь прописан в локальный конфиг (~/.kube/config, блок users)
 * пользователь может просматривать логи подов и их конфигурацию (kubectl logs pod <pod_id>, kubectl describe pod <pod_id>)

Роль с нужными правами:
```YAML
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: log-viewer
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list", "describe", "logs"]
```

```bash

# создаём пользователя
root@ubuntu-server# kubectl create serviceaccount netology-new
serviceaccount/netology-new created

# привязываем пользователя к роли
root@ubuntu-server# kubectl create rolebinding log-viewer --clusterrole=view --serviceaccount=default:netology-new --namespace=default
rolebinding.rbac.authorization.k8s.io/log-viewer created

# создаём токен для пользователя
root@ubuntu-server# kubectl apply -f - <<EOF
> apiVersion: v1
> kind: Secret
> metadata:
>   name: netology-new
>   annotations:
>     kubernetes.io/service-account.name: netology-new
> type: kubernetes.io/service-account-token
> EOF
secret/netology-new created

# смотрим созданный токен
root@ubuntu-server# kubectl describe secret/netology-new
Name:         netology-new
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: netology-new
              kubernetes.io/service-account.uid: 5c7eb0cf-5dd9-42b6-a458-9930939436c2

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1111 bytes
namespace:  7 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IkhxX2RpVkN5WkFvLW9PUllFMGw0d3FKdHZtZEJScUpLOUtWZjJnb0NsamsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im5ldG9sb2d5LW5ldyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuZXRvbG9neS1uZXciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI1YzdlYjBjZi01ZGQ5LTQyYjYtYTQ1OC05OTMwOTM5NDM2YzIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpuZXRvbG9neS1uZXcifQ.z3Z9bCGABWc3apCHFT4EJur5IQsrmFVEzky9uxZrEEKuXthDxnLgqmIF_7sBcFf2cFWsPJnFyEeECUxp4myyATls9yh7vm4JudZmzWmRIiV0qrOJNIr5Me3gABLxfYyJ8J0UUVZhLo8lVrdPXbMUEXEcuACqmcw25OT2I6hI9LLUr4BAksQsM3WMKg77H_X3JQ16ug32UkVXeIrfyhJ9uAM9iMojRAZGKzL700AArez7nxB4YxIvy43mNgVCcmNLZA7bvlkrd42g08tRB1AMCOyMWx73YncfxHkfpqoYl779PSwDHd_zlvewUj7uerEzH1Jy3gMoQKv33s3hIqDElg

# добавляем пользователя с токеном в конфиг
root@ubuntu-server# kubectl config set-credentials netology-new --token eyJhbGciOiJSUzI1NiIsImtpZCI6IkhxX2RpVkN5WkFvLW9PUllFMGw0d3FKdHZtZEJScUpLOUtWZjJnb0NsamsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im5ldG9sb2d5LW5ldyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuZXRvbG9neS1uZXciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI1YzdlYjBjZi01ZGQ5LTQyYjYtYTQ1OC05OTMwOTM5NDM2YzIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpuZXRvbG9neS1uZXcifQ.z3Z9bCGABWc3apCHFT4EJur5IQsrmFVEzky9uxZrEEKuXthDxnLgqmIF_7sBcFf2cFWsPJnFyEeECUxp4myyATls9yh7vm4JudZmzWmRIiV0qrOJNIr5Me3gABLxfYyJ8J0UUVZhLo8lVrdPXbMUEXEcuACqmcw25OT2I6hI9LLUr4BAksQsM3WMKg77H_X3JQ16ug32UkVXeIrfyhJ9uAM9iMojRAZGKzL700AArez7nxB4YxIvy43mNgVCcmNLZA7bvlkrd42g08tRB1AMCOyMWx73YncfxHkfpqoYl779PSwDHd_zlvewUj7uerEzH1Jy3gMoQKv33s3hIqDElg
User "netology-new" set.

# настраиваем контекст на работу с новым пользователем
root@ubuntu-server# kubectl config set-context minikube --user netology-new
Context "minikube" modified.

# переключаемся на контекст
root@ubuntu-server# kubectl config use-context minikube
Switched to context "minikube".

# пробуем посмотреть поды (успешно)
root@ubuntu-server# kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-7567d9fdc9-8jmln   1/1     Running   0          44m
hello-node-7567d9fdc9-d8vcr   1/1     Running   0          44m
hello-node-7567d9fdc9-dwg9l   1/1     Running   0          44m
hello-node-7567d9fdc9-f767q   1/1     Running   0          44m
hello-node-7567d9fdc9-js9kj   1/1     Running   0          44m

# пробуем удалить какой-нибудь под (не хватает прав)
root@ubuntu-server# kubectl delete pods/hello-node-7567d9fdc9-d8vcr
Error from server (Forbidden): pods "hello-node-7567d9fdc9-d8vcr" is forbidden: User "system:serviceaccount:default:netology-new" cannot delete resource "pods" in API group "" in the namespace "default"

# возвращшаем стандартного пользователя в контекст
root@ubuntu-server# kubectl config set-context minikube --user minikube
Context "minikube" modified.

# теперь можно и удалять поды
root@ubuntu-server# kubectl delete pods/hello-node-7567d9fdc9-d8vcr
pod "hello-node-7567d9fdc9-d8vcr" deleted
```


## Задание 3: Изменение количества реплик 
Поработав с приложением, вы получили запрос на увеличение количества реплик приложения для нагрузки. Необходимо изменить запущенный deployment, увеличив количество реплик до 5. Посмотрите статус запущенных подов после увеличения реплик. 

Требования:
 * в deployment из задания 1 изменено количество реплик на 5
 * проверить что все поды перешли в статус running (kubectl get pods)

```
root@ubuntu-server:~# kubectl scale --replicas=5 deployment/hello-node
root@ubuntu-server:~# kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-7567d9fdc9-b562k   1/1     Running   0          6s
hello-node-7567d9fdc9-g4ssk   1/1     Running   0          6s
hello-node-7567d9fdc9-lwp2k   1/1     Running   0          6s
hello-node-7567d9fdc9-xgglb   1/1     Running   0          2d22h
hello-node-7567d9fdc9-xs5nm   1/1     Running   0          2d22h
```
