# Домашнее задание к занятию "12.5 Сетевые решения CNI"
После работы с Flannel появилась необходимость обеспечить безопасность для приложения. Для этого лучше всего подойдет Calico.
## Задание 1: установить в кластер CNI плагин Calico
Для проверки других сетевых решений стоит поставить отличный от Flannel плагин — например, Calico. Требования: 
* установка производится через ansible/kubespray;
* после применения следует настроить политику доступа к hello world извне.

```bash
# сделаем поды деплоймента доступными из вне кластера, создав сервис
root@node1:~# kubectl expose deployment hello-node --type=LoadBalancer --port=8080

# посмотрим на какой порт проброшено приложение
root@node1:~# kubectl get service
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-node   LoadBalancer   10.233.15.167   <pending>     8080:31165/TCP   28m
```
Обратимся к приложению по внешним ip нод кластера и данному порту:
![image](https://user-images.githubusercontent.com/32748936/120618391-b573be80-c463-11eb-887f-8fb1549312d0.png)
![image](https://user-images.githubusercontent.com/32748936/120618421-bc9acc80-c463-11eb-8437-4216d4a2f70f.png)

## Задание 2: изучить, что запущено по умолчанию
Самый простой способ — проверить командой calicoctl get <type>. Для проверки стоит получить список нод, ipPool и profile.
Требования: 
* установить утилиту calicoctl;
* получить 3 вышеописанных типа в консоли.

![image](https://user-images.githubusercontent.com/32748936/120483917-3aef6400-c3bb-11eb-8d4a-8fecb0081ca7.png)
