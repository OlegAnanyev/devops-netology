
# Домашнее задание к занятию "11.04 Микросервисы: масштабирование"

Вы работаете в крупной компанию, которая строит систему на основе микросервисной архитектуры.
Вам как DevOps специалисту необходимо обеспечить следующее.

## Задача 1: Распределенный кэш

Разработчикам вашей компании понадобился распределенный кэш для организации хранения временной информации по сессиям пользователей.
Вам необходимо построить Redis Cluster состоящий из трех шард с тремя репликами.

### Схема:

![11-04-01](https://user-images.githubusercontent.com/1122523/114282923-9b16f900-9a4f-11eb-80aa-61ed09725760.png)

```
В задании на схеме показано, что шарды и реплики должны быть разнесены на 3 виртуальные машины, но для целей
выполнения ДЗ я разместил сервера Redis в 6 докер-контейнеров. Их, в свою очередь, можно разделять по
физическим/виртуальным машинам как угодно.

docker-compose и конфиги серверов: https://github.com/OlegAnanyev/devops-netology/tree/master/homeworks/11-microservices-04-scaling
Успешно созданный кластер: http://prntscr.com/1313kl8
```

```bash
root@b45283683569:/data# redis-cli --cluster create 173.17.0.2:7002 173.17.0.3:7003 173.17.0.4:7004 173.17.0.5:7005 173.17.0.6:7006 173.17.0.7:7007 --cluster-replicas 1
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 173.17.0.6:7006 to 173.17.0.2:7002
Adding replica 173.17.0.7:7007 to 173.17.0.3:7003
Adding replica 173.17.0.5:7005 to 173.17.0.4:7004
M: 94adfc3f4946f3afc41d4c852562b57b8fc6dc7f 173.17.0.2:7002
   slots:[0-5460] (5461 slots) master
M: fe3507f13a75fb7580869c299cc563bf9063d07c 173.17.0.3:7003
   slots:[5461-10922] (5462 slots) master
M: c68c7d1eb69f593ccdd33ffdcf3fbd1b894d1652 173.17.0.4:7004
   slots:[10923-16383] (5461 slots) master
S: d73ce79938e9be3d7899be857ba6065a6a2d1b83 173.17.0.5:7005
   replicates c68c7d1eb69f593ccdd33ffdcf3fbd1b894d1652
S: 88be6f89538fabd64ebdceb9fb76ebbba53ae35f 173.17.0.6:7006
   replicates 94adfc3f4946f3afc41d4c852562b57b8fc6dc7f
S: 003b2a69c7fedd6b881e3a6160ca30785cf9d153 173.17.0.7:7007
   replicates fe3507f13a75fb7580869c299cc563bf9063d07c
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
.
>>> Performing Cluster Check (using node 173.17.0.2:7002)
M: 94adfc3f4946f3afc41d4c852562b57b8fc6dc7f 173.17.0.2:7002
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: 003b2a69c7fedd6b881e3a6160ca30785cf9d153 173.17.0.7:7007
   slots: (0 slots) slave
   replicates fe3507f13a75fb7580869c299cc563bf9063d07c
S: 88be6f89538fabd64ebdceb9fb76ebbba53ae35f 173.17.0.6:7006
   slots: (0 slots) slave
   replicates 94adfc3f4946f3afc41d4c852562b57b8fc6dc7f
M: fe3507f13a75fb7580869c299cc563bf9063d07c 173.17.0.3:7003
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: c68c7d1eb69f593ccdd33ffdcf3fbd1b894d1652 173.17.0.4:7004
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: d73ce79938e9be3d7899be857ba6065a6a2d1b83 173.17.0.5:7005
   slots: (0 slots) slave
   replicates c68c7d1eb69f593ccdd33ffdcf3fbd1b894d1652
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

```

