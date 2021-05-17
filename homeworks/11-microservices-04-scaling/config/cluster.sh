#зайдём в терминал
docker exec -it redis-cluster_tester_1 /bin/bash

#создадим кластер
redis-cli --cluster create 173.17.0.2:7002 173.17.0.3:7003 173.17.0.4:7004 173.17.0.5:7005 173.17.0.6:7006 173.17.0.7:7007 --cluster-replicas 1 --cluster-yes