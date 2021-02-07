# Домашнее задание к занятию "10.03. Grafana"

## Задание повышенной сложности

**В части задания 1** не используйте директорию [help](./help) для сборки проекта, самостоятельно разверните grafana, где в 
роли источника данных будет выступать prometheus, а сборщиком данных node-exporter:
- grafana
- prometheus-server
- prometheus node-exporter

За дополнительными материалами, вы можете обратиться в официальную документацию grafana и prometheus.

В решении к домашнему заданию приведите также все конфигурации/скрипты/манифесты, которые вы 
использовали в процессе решения задания.

**В части задания 3** вы должны самостоятельно завести удобный для вас канал нотификации, например Telegram или Email
и отправить туда тестовые события.

В решении приведите скриншоты тестовых событий из каналов нотификаций.

## Обязательные задания

### Задание 1
Используя директорию [help](./help) внутри данного домашнего задания - запустите связку prometheus-grafana.

Зайдите в веб-интерфейс графана, используя авторизационные данные, указанные в манифесте docker-compose.

Подключите поднятый вами prometheus как источник данных.

Решение домашнего задания - скриншот веб-интерфейса grafana со списком подключенных Datasource.

## Задание 2
Изучите самостоятельно ресурсы:
- [promql-for-humans](https://timber.io/blog/promql-for-humans/#cpu-usage-by-instance)
- [understanding prometheus cpu metrics](https://www.robustperception.io/understanding-machine-cpu-usage)

Создайте Dashboard и в ней создайте следующие Panels:
- Утилизация CPU для nodeexporter (в процентах, 100-idle)
```
(((count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu))) - avg(sum by (mode)(irate(node_cpu_seconds_total{mode='idle',instance="$node",job="$job"}[5m])))) * 100) / count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu))
```
- CPULA 1/5/15
```
avg(node_load1{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100

avg(node_load5{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100

avg(node_load15{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100
```
- Количество свободной оперативной памяти
```
(node_memory_MemAvailable_bytes{instance="$node",job="$job"} * 100) / node_memory_MemTotal_bytes{instance="$node",job="$job"}
```
- Количество места на файловой системе
```
(node_filesystem_avail_bytes{instance="$node",job="$job",mountpoint="/",fstype!="rootfs"} * 100) / node_filesystem_size_bytes{instance="$node",job="$job",mountpoint="/",fstype!="rootfs"}
```
Для решения данного ДЗ приведите promql запросы для выдачи этих метрик, а также скриншот получившейся Dashboard.

## Задание 3
Создайте для каждой Dashboard подходящее правило alert (можно обратиться к первой лекции в блоке "Мониторинг").

Для решения ДЗ - приведите скриншот вашей итоговой Dashboard.

## Задание 4
Сохраните ваш Dashboard.

Для этого перейдите в настройки Dashboard, выберите в боковом меню "JSON MODEL".

Далее скопируйте отображаемое json-содержимое в отдельный файл и сохраните его.

В решении задания - приведите листинг этого файла.
```json
{
  "annotations": {
    "list": [
      {
        "$$hashKey": "object:1058",
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": 1860,
  "graphTooltip": 0,
  "id": 3,
  "iteration": 1612711147326,
  "links": [],
  "panels": [
    {
      "collapsed": false,
      "datasource": "Prometheus",
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 261,
      "panels": [],
      "repeat": null,
      "title": "Quick CPU / Mem / Disk",
      "type": "row"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "mappings": [
            {
              "id": 0,
              "op": "=",
              "text": "N/A",
              "type": 1,
              "value": "null"
            }
          ],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 80
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 90
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 3,
        "x": 0,
        "y": 1
      },
      "id": 154,
      "links": [],
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "text": {},
        "textMode": "auto"
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "(node_filesystem_avail_bytes{instance=\"$node\",job=\"$job\",mountpoint=\"/\",fstype!=\"rootfs\"} * 100) / node_filesystem_size_bytes{instance=\"$node\",job=\"$job\",mountpoint=\"/\",fstype!=\"rootfs\"}",
          "format": "time_series",
          "interval": "",
          "intervalFactor": 1,
          "legendFormat": "",
          "refId": "A",
          "step": 900
        }
      ],
      "title": "DISK SPACE FREE",
      "type": "stat"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "mappings": [
            {
              "id": 0,
              "op": "=",
              "text": "N/A",
              "type": 1,
              "value": "null"
            }
          ],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 85
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 95
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 3,
        "x": 3,
        "y": 1
      },
      "id": 155,
      "links": [],
      "options": {
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true,
        "text": {}
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "avg(node_load1{instance=\"$node\",job=\"$job\"}) /  count(count(node_cpu_seconds_total{instance=\"$node\",job=\"$job\"}) by (cpu)) * 100",
          "format": "time_series",
          "hide": false,
          "interval": "",
          "intervalFactor": 1,
          "legendFormat": "",
          "refId": "A",
          "step": 900
        }
      ],
      "title": "CPU LA 1m",
      "type": "gauge"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "mappings": [
            {
              "id": 0,
              "op": "=",
              "text": "N/A",
              "type": 1,
              "value": "null"
            }
          ],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 85
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 95
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 3,
        "x": 6,
        "y": 1
      },
      "id": 316,
      "links": [],
      "options": {
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true,
        "text": {}
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "avg(node_load5{instance=\"$node\",job=\"$job\"}) /  count(count(node_cpu_seconds_total{instance=\"$node\",job=\"$job\"}) by (cpu)) * 100",
          "format": "time_series",
          "hide": false,
          "intervalFactor": 1,
          "refId": "A",
          "step": 900
        }
      ],
      "title": "CPU LA 5m",
      "type": "gauge"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "mappings": [
            {
              "id": 0,
              "op": "=",
              "text": "N/A",
              "type": 1,
              "value": "null"
            }
          ],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 85
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 95
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 3,
        "x": 9,
        "y": 1
      },
      "id": 19,
      "links": [],
      "options": {
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true,
        "text": {}
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "avg(node_load15{instance=\"$node\",job=\"$job\"}) /  count(count(node_cpu_seconds_total{instance=\"$node\",job=\"$job\"}) by (cpu)) * 100",
          "hide": false,
          "intervalFactor": 1,
          "refId": "A",
          "step": 900
        }
      ],
      "title": "CPU LA 15m",
      "type": "gauge"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "mappings": [
            {
              "id": 0,
              "op": "=",
              "text": "N/A",
              "type": 1,
              "value": "null"
            }
          ],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 85
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 95
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 0,
        "y": 8
      },
      "id": 20,
      "links": [],
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "text": {},
        "textMode": "auto"
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "(((count(count(node_cpu_seconds_total{instance=\"$node\",job=\"$job\"}) by (cpu))) - avg(sum by (mode)(irate(node_cpu_seconds_total{mode='idle',instance=\"$node\",job=\"$job\"}[5m])))) * 100) / count(count(node_cpu_seconds_total{instance=\"$node\",job=\"$job\"}) by (cpu))",
          "hide": false,
          "interval": "",
          "intervalFactor": 1,
          "legendFormat": "",
          "refId": "A",
          "step": 900
        }
      ],
      "title": "CPU UTIL",
      "type": "stat"
    },
    {
      "cacheTimeout": null,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "custom": {},
          "decimals": 0,
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "rgba(50, 172, 45, 0.97)",
                "value": null
              },
              {
                "color": "rgba(237, 129, 40, 0.89)",
                "value": 80
              },
              {
                "color": "rgba(245, 54, 54, 0.9)",
                "value": 90
              }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 6,
        "y": 8
      },
      "hideTimeOverride": false,
      "id": 16,
      "links": [],
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "text": {},
        "textMode": "auto"
      },
      "pluginVersion": "7.4.0",
      "targets": [
        {
          "expr": "((node_memory_MemTotal_bytes{instance=\"$node\",job=\"$job\"} - node_memory_MemFree_bytes{instance=\"$node\",job=\"$job\"}) / (node_memory_MemTotal_bytes{instance=\"$node\",job=\"$job\"} )) * 100",
          "format": "time_series",
          "hide": true,
          "intervalFactor": 1,
          "refId": "A",
          "step": 900
        },
        {
          "expr": "(node_memory_MemAvailable_bytes{instance=\"$node\",job=\"$job\"} * 100) / node_memory_MemTotal_bytes{instance=\"$node\",job=\"$job\"}",
          "format": "time_series",
          "hide": false,
          "interval": "",
          "intervalFactor": 1,
          "legendFormat": "",
          "refId": "B",
          "step": 900
        }
      ],
      "title": "RAM FREE",
      "type": "stat"
    },
    {
      "cacheTimeout": null,
      "colorBackground": false,
      "colorValue": false,
      "colors": [
        "rgba(245, 54, 54, 0.9)",
        "rgba(237, 129, 40, 0.89)",
        "rgba(50, 172, 45, 0.97)"
      ],
      "datasource": "Prometheus",
      "decimals": 1,
      "description": "",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "format": "s",
      "gauge": {
        "maxValue": 100,
        "minValue": 0,
        "show": false,
        "thresholdLabels": false,
        "thresholdMarkers": true
      },
      "gridPos": {
        "h": 5,
        "w": 12,
        "x": 0,
        "y": 15
      },
      "hideTimeOverride": true,
      "id": 15,
      "interval": null,
      "links": [],
      "mappingType": 1,
      "mappingTypes": [
        {
          "$$hashKey": "object:1094",
          "name": "value to text",
          "value": 1
        },
        {
          "$$hashKey": "object:1095",
          "name": "range to text",
          "value": 2
        }
      ],
      "maxDataPoints": 100,
      "nullPointMode": "null",
      "nullText": null,
      "postfix": "s",
      "postfixFontSize": "50%",
      "prefix": "",
      "prefixFontSize": "50%",
      "rangeMaps": [
        {
          "from": "null",
          "text": "N/A",
          "to": "null"
        }
      ],
      "sparkline": {
        "fillColor": "rgba(31, 118, 189, 0.18)",
        "full": false,
        "lineColor": "rgb(31, 120, 193)",
        "show": false
      },
      "tableColumn": "",
      "targets": [
        {
          "expr": "node_time_seconds{instance=\"$node\",job=\"$job\"} - node_boot_time_seconds{instance=\"$node\",job=\"$job\"}",
          "intervalFactor": 2,
          "refId": "A",
          "step": 1800
        }
      ],
      "thresholds": "",
      "title": "UPTIME",
      "type": "singlestat",
      "valueFontSize": "50%",
      "valueMaps": [
        {
          "$$hashKey": "object:1097",
          "op": "=",
          "text": "N/A",
          "value": "null"
        }
      ],
      "valueName": "current"
    }
  ],
  "refresh": "1m",
  "schemaVersion": 27,
  "style": "dark",
  "tags": [
    "linux"
  ],
  "templating": {
    "list": [
      {
        "current": {
          "selected": false,
          "text": "Prometheus",
          "value": "Prometheus"
        },
        "description": null,
        "error": null,
        "hide": 0,
        "includeAll": false,
        "label": "datasource",
        "multi": false,
        "name": "DS_PROMETHEUS",
        "options": [],
        "query": "prometheus",
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "type": "datasource"
      },
      {
        "allValue": null,
        "current": {
          "selected": false,
          "text": "node_localhost",
          "value": "node_localhost"
        },
        "datasource": "Prometheus",
        "definition": "",
        "description": null,
        "error": null,
        "hide": 0,
        "includeAll": false,
        "label": "Job",
        "multi": false,
        "name": "job",
        "options": [],
        "query": {
          "query": "label_values(node_uname_info, job)",
          "refId": "Prometheus-job-Variable-Query"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "sort": 1,
        "tagValuesQuery": "",
        "tags": [],
        "tagsQuery": "",
        "type": "query",
        "useTags": false
      },
      {
        "allValue": null,
        "current": {
          "selected": false,
          "text": "localhost:9100",
          "value": "localhost:9100"
        },
        "datasource": "Prometheus",
        "definition": "label_values(node_uname_info{job=\"$job\"}, instance)",
        "description": null,
        "error": null,
        "hide": 0,
        "includeAll": false,
        "label": "Host:",
        "multi": false,
        "name": "node",
        "options": [],
        "query": {
          "query": "label_values(node_uname_info{job=\"$job\"}, instance)",
          "refId": "Prometheus-node-Variable-Query"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "sort": 1,
        "tagValuesQuery": "",
        "tags": [],
        "tagsQuery": "",
        "type": "query",
        "useTags": false
      },
      {
        "allValue": null,
        "current": {
          "selected": false,
          "text": "[a-z]+|nvme[0-9]+n[0-9]+",
          "value": "[a-z]+|nvme[0-9]+n[0-9]+"
        },
        "description": null,
        "error": null,
        "hide": 2,
        "includeAll": false,
        "label": null,
        "multi": false,
        "name": "diskdevices",
        "options": [
          {
            "selected": true,
            "text": "[a-z]+|nvme[0-9]+n[0-9]+",
            "value": "[a-z]+|nvme[0-9]+n[0-9]+"
          }
        ],
        "query": "[a-z]+|nvme[0-9]+n[0-9]+",
        "skipUrlSync": false,
        "type": "custom"
      }
    ]
  },
  "time": {
    "from": "now-24h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "5s",
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ],
    "time_options": [
      "5m",
      "15m",
      "1h",
      "6h",
      "12h",
      "24h",
      "2d",
      "7d",
      "30d"
    ]
  },
  "timezone": "browser",
  "title": "OlegAnanyev Netology Dashboard",
  "uid": "rYdddlPWk",
  "version": 10
}
```
