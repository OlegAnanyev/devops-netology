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

Логи: (https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/log_corretto.png)

Веб-интефейс: (https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/screen_corretto.png)

- Образ: 

[https://hub.docker.com/repository/docker/olegananyev/jenkins-corretto](https://hub.docker.com/repository/docker/olegananyev/jenkins-corretto)

---------------------------
- Dockerfile Ubuntu:

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

Логи: (https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/log_ubuntu.png)

Веб-интефейс: (https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/screen_ubuntu.png)

- Образ: 

[https://hub.docker.com/repository/docker/olegananyev/jenkins-ubuntu](https://hub.docker.com/repository/docker/olegananyev/jenkins-ubuntu)


## Задача 3 

- Dockerfile:

```
FROM node
ADD https://github.com/simplicitesoftware/nodejs-demo/archive/master.zip /
RUN unzip master.zip && \
    cd /nodejs-demo-master && \
    npm install
EXPOSE 3000
WORKDIR "/nodejs-demo-master"
CMD ["npm", "start", "0.0.0.0"]
```

- Список сетей:

```
07:35:24 hawk@ubuntu-server ~ → docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
66de3a38b069        bridge              bridge              local
f1b555ae580e        host                host                local
d60169761a06        node_network        bridge              local
9cc68b3eca05        none                null                local
```

- Подробности по сети node_network:

```
07:41:35 hawk@ubuntu-server ~ → docker network inspect node_network
[
    {
        "Name": "node_network",
        "Id": "d60169761a06705ec36544d0d49c7bbf2c3bff96e744058a40c3bfb3632999ca",
        "Created": "2020-10-17T19:33:39.902392136+03:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "1e1b27c38e0b34560f5b48f2f4cfb7c4303cf07dfceb2551c081f80990e533bd": {
                "Name": "cool_blackwell",
                "EndpointID": "22385ec1a4a7f806a968f2820bd7007ae710da138f8d3c88be34ad6b98acf05d",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            },
            "57e80454c31886f320cc18d9b7aa75212e51cf97b2fdf6e950c6219dc112cbca": {
                "Name": "flamboyant_jang",
                "EndpointID": "38838f18d847da8866d4b1473fbe34014bd6e91970440323d14df55ef51e7b77",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]

```

- Скриншот curl:

Скриншот: (https://raw.githubusercontent.com/OlegAnanyev/devops-netology/master/homeworks/curl_node.png)
