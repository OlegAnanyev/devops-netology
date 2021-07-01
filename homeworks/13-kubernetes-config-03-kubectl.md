# Домашнее задание к занятию "13.3 работа с kubectl"
## Задание 1: проверить работоспособность каждого компонента
Для проверки работы можно использовать 2 способа: port-forward и exec. Используя оба способа, проверьте каждый компонент:
* сделайте запросы к бекенду;
* сделайте запросы к фронту;
* подключитесь к базе данных.

```
exec:
```

```bash
root@node1:~# k exec -it backend-bdbd584cf-fwvfz -- curl localhost:9000
{"detail":"Not Found"}


root@node1:~# k exec -it frontend-6576f7dd68-84hgs -- curl localhost:80
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>

root@node1:~# k exec -it db-0 -- /bin/bash
bash-5.1# su postgres
/ $ psql -h localhost news
psql (13.3)
Type "help" for help.

news=#
```

```
port-forward:
```

![image](https://user-images.githubusercontent.com/32748936/124096281-1abacf80-da63-11eb-8c20-06cc033efd7a.png)


## Задание 2: ручное масштабирование
При работе с приложением иногда может потребоваться вручную добавить пару копий. Используя команду kubectl scale, попробуйте увеличить количество бекенда и фронта до 3. После уменьшите количество копий до 1. Проверьте, на каких нодах оказались копии после каждого действия (kubectl describe).

```
root@node1:~# k get nodes
NAME    STATUS   ROLES                  AGE   VERSION
node1   Ready    control-plane,master   34d   v1.20.7
node2   Ready    <none>                 34d   v1.20.7
```    
![image](https://user-images.githubusercontent.com/32748936/124098855-9b7acb00-da65-11eb-8427-62e773c90ca4.png)

```
Видимо из-за легковесности приложений они все запускаются на node2
```

