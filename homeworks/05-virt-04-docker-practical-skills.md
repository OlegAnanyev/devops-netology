# Домашнее задание к занятию "5.4. Практические навыки работы с Docker"

## Задача 1 
- Dockerfile:

```
FROM centos:centos7
ADD http://github.com/erkin/ponysay/archive/master.tar.gz /
RUN yum check-update && \
    yum install -y texinfo python3 && \
    tar -xzf master.tar.gz && \
    cd ponysay-master && \
    ./setup.py install --freedom=partial && \
     rm -rf /master.tar.gz /ponysay-master
ENTRYPOINT ["/usr/bin/ponysay"]
CMD ["Hey, netology"]
```

- Скриншот:

![Скриншот](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/05-virt-04-docker-practical-skills-1v1.png)

- Образ: 

[https://hub.docker.com/r/olegananyev/ponysay-centos](https://hub.docker.com/r/olegananyev/ponysay-centos)



## Задача 2 
- Dockerfile Corretto:

```
FROM amazoncorretto
ADD https://pkg.jenkins.io/redhat-stable/jenkins.repo /etc/yum.repos.d/
RUN rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key && \
    yum install -y jenkins
CMD ["java", "-jar", "/usr/lib/jenkins/jenkins.war"]
```

- Скриншоты:

![Логи](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/log_corretto.png =700x)

![Веб-интефейс](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/screen_corretto.png =700x)

- Образ: 

[https://hub.docker.com/repository/docker/olegananyev/jenkins-corretto](https://hub.docker.com/repository/docker/olegananyev/jenkins-corretto)

---------------------------
- Dockerfile Corretto:

```
FROM ubuntu:latest
ADD https://pkg.jenkins.io/debian-stable/jenkins.io.key /
RUN apt-get update && \
    apt-get install -y gnupg ca-certificates && \
    apt-key add /jenkins.io.key && \
    sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list' && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk openjdk-8-jre jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
```

- Скриншоты:

![Логи](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/05-virt-04-docker-practical-skills-1v1.png)

![Веб-интефейс](https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/05-virt-04-docker-practical-skills-1v1.png)

- Образ: 

[https://hub.docker.com/repository/docker/olegananyev/jenkins-ubuntu](https://hub.docker.com/repository/docker/olegananyev/jenkins-ubuntu)


## Задача 3 

В данном задании вы научитесь:
- объединять контейнеры в единую сеть
- исполнять команды "изнутри" контейнера

Для выполнения задания вам нужно:
- Написать Dockerfile: 
    - Использовать образ https://hub.docker.com/_/node как базовый
    - Установить необходимые зависимые библиотеки для запуска npm приложения https://github.com/simplicitesoftware/nodejs-demo
    - Выставить у приложения (и контейнера) порт 3000 для прослушки входящих запросов  
    - Соберите образ и запустите контейнер в фоновом режиме с публикацией порта

- Запустить второй контейнер из образа ubuntu:latest 
- Создайть `docker network` и добавьте в нее оба запущенных контейнера
- Используя `docker exec` запустить командную строку контейнера `ubuntu` в интерактивном режиме
- Используя утилиту `curl` вызвать путь `/` контейнера с npm приложением  

Для получения зачета, вам необходимо предоставить:
- Наполнение Dockerfile с npm приложением
- Скриншот вывода вызова команды списка docker сетей (docker network cli)
- Скриншот вызова утилиты curl с успешным ответом
