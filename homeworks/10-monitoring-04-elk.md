# Домашнее задание к занятию "10.04. ELK"

В процессе выполнения задания могут возникнуть также не указанные тут проблемы в зависимости от системы.
Используйте output stdout filebeat/kibana и api elasticsearch для изучения корня проблемы и ее устранения.

## Задание повышенной сложности

Не используйте директорию [help](./help) при выполнении домашнего задания.

## Задание 1

Вам необходимо поднять в докере:
- elasticsearch(hot и warm ноды)
- logstash
- kibana
- filebeat

и связать их между собой.

Logstash следует сконфигурировать для приёма по tcp json сообщений.

Filebeat следует сконфигурировать для отправки логов docker вашей системы в logstash.

В директории [help](./help) находится манифест docker-compose и конфигурации filebeat/logstash для быстрого 
выполнения данного задания.

Результатом выполнения данного задания должны быть:
- скриншот `docker ps` через 5 минут после старта всех контейнеров (их должно быть 5)
```
http://prntscr.com/10892sd
```
- скриншот интерфейса kibana
```
http://prntscr.com/10890d6
```
- docker-compose манифест (если вы не использовали директорию help)
```
version: '2.2'
services:

  es-hot:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.11.0
    container_name: es-hot
    environment:
      - node.name=es-hot
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es-warm
      - cluster.initial_master_nodes=es-hot,es-warm
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - data01:/usr/share/elasticsearch/data:Z
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
    networks:
      - elastic
    depends_on:
      - es-warm

  es-warm:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.11.0
    container_name: es-warm
    environment:
      - node.name=es-warm
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es-hot
      - cluster.initial_master_nodes=es-hot,es-warm
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - data02:/usr/share/elasticsearch/data:Z
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    networks:
      - elastic

  kibana:
    image: docker.elastic.co/kibana/kibana:7.11.0
    container_name: kibana
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://es-hot:9200
      ELASTICSEARCH_HOSTS: '["http://es-hot:9200","http://es-warm:9200"]'
    networks:
      - elastic
    depends_on:
      - es-hot
      - es-warm

  logstash:
    image: docker.elastic.co/logstash/logstash:6.3.2
    container_name: logstash
    ports:
      - 5044:5044
    volumes:
      - ./configs/logstash.yml:/opt/logstash/config/logstash.yml:Z      
# это не тот путь!      
#      - ./configs/logstash.conf:/etc/logstash/conf.d/logstash.conf:Z

# а вот это правильный!
      - ./configs/logstash.conf:/usr/share/logstash/pipeline/logstash.conf:Z

    networks:
      - elastic
    depends_on:
      - es-hot
      - es-warm

  filebeat:
    image: "docker.elastic.co/beats/filebeat:7.2.0"
    container_name: filebeat
    privileged: true
    user: root
    volumes:
      - ./configs/filebeat.yml:/usr/share/filebeat/filebeat.yml:Z
      - /var/lib/docker:/var/lib/docker:Z
      - /var/run/docker.sock:/var/run/docker.sock:Z
    networks:
      - elastic
    depends_on:
      - logstash

  some_application:
    image: library/python:3.9-alpine
    container_name: some_app
    volumes:
      - ./pinger/run.py:/opt/run.py:Z
    entrypoint: python3 /opt/run.py

volumes:
  data01:
    driver: local
  data02:
    driver: local
  data03:
    driver: local

networks:
  elastic:
    driver: bridge
```
- ваши yml конфигурации для стека (если вы не использовали директорию help)

logstash.conf:
```
input {
  beats {
    port => 5044
  }
}
filter {
  json {
    source => "message"
  }
  date{
    match => ["timestamp", "UNIX_MS"]
    target => "@timestamp"
  }
  ruby {
    code => "event.set('indexDay', event.get('[@timestamp]').time.localtime('+09:00').strftime('%Y%m%d'))"
  }
}
output {
  elasticsearch {
    hosts => ["es-hot:9200"]
    index => "logstash-%{indexDay}"
    codec => json
  }
  stdout {
    codec => rubydebug
  }
}
```

filebeat.yml
```
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'

processors:
  - add_docker_metadata:
      host: "unix:///var/run/docker.sock"

  - decode_json_fields:
      fields: ["message"]
      target: "json"
      overwrite_keys: true

output.logstash:
  hosts: ["logstash:5044"]

#output.console:
#  enabled: true

logging.json: true
logging.metrics.enabled: false

```

## Задание 2

Перейдите в меню [создания index-patterns  в kibana](http://localhost:5601/app/management/kibana/indexPatterns/create)
и создайте несколько index-patterns из имеющихся.

Перейдите в меню просмотра логов в kibana (Discover) и самостоятельно изучите как отображаются логи и как производить 
поиск по логам.

В манифесте директории help также приведенно dummy приложение, которое генерирует рандомные события в stdout контейнера.
Данные логи должны порождать индекс logstash-* в elasticsearch. Если данного индекса нет - воспользуйтесь советами 
и источниками из раздела "Дополнительные ссылки" данного ДЗ.

```
http://prntscr.com/10894ut
```
 

 
