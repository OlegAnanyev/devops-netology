# Домашнее задание к занятию "12.4 Развертывание кластера на собственных серверах, лекция 2"
Новые проекты пошли стабильным потоком. Каждый проект требует себе несколько кластеров: под тесты и продуктив. Делать все руками — не вариант, поэтому стоит автоматизировать подготовку новых кластеров.

## Задание 1: Подготовить инвентарь kubespray
Новые тестовые кластеры требуют типичных простых настроек. Нужно подготовить инвентарь и проверить его работу. Требования к инвентарю:
* подготовка работы кластера из 5 нод: 1 мастер и 4 рабочие ноды;
* в качестве CRI — containerd;
* запуск etcd производить на мастере.

----------------------------------------


Мой inventory (рабочая нода только одна, чтобы не поднимать лишние виртуалки):
```ini
node1 ansible_host=192.168.52.148  etcd_member_name=etcd1
node2 ansible_host=192.168.52.149

[kube_control_plane]
node1

[etcd]
node1

[kube_node]
node2

[calico_rr]

[k8s_cluster:children]
kube_control_plane
kube_node
calico_rr
```

```
Для установки на Ubuntu Server 20.04.2 LTS пришлось подправить файл \roles\kubernetes\preinstall\vars\ubuntu.yml, изменив 
required_pkgs:
  - python-apt

на

required_pkgs:
  - python3-apt
  
для использования containerd:
## k8s_cluster.yml
container_manager: containerd

## etcd.yml
etcd_deployment_type: host

## Containerd config

containerd_registries:
  "docker.io":
    - "https://mirror.gcr.io"
    - "https://registry-1.docker.io"
```

Запускаем плейбук:
```
ansible-playbook -i kubespray/inventory/dz-cluster/inventory.ini kubespray/cluster.yml -u hawk --ask-pass -b --ask-become-pass
```
Результат выполнения плейбука:
![image](https://user-images.githubusercontent.com/32748936/119849047-f8d6a600-bf14-11eb-8db1-8487de647736.png)

Проверяем кластер с мастер-ноды:
![image](https://user-images.githubusercontent.com/32748936/119849331-33d8d980-bf15-11eb-8de1-3b5f1b6cb0aa.png)



## Задание 2 (*): подготовить и проверить инвентарь для кластера в AWS
Часть новых проектов хотят запускать на мощностях AWS. Требования похожи:
* разворачивать 5 нод: 1 мастер и 4 рабочие ноды;
* работать должны на минимально допустимых EC2 — t3.small.

---------------------------------------

Уменьшим требования к памяти для маcтеров и воркеров в файле kubespray\roles\kubernetes\preinstall\defaults\main.yml:

```yaml
# Minimal memory requirement in MB for safety checks
minimal_node_memory_mb: 900
minimal_master_memory_mb: 900
```

![image](https://user-images.githubusercontent.com/32748936/120026606-fbabc680-bffa-11eb-913f-fa2352d2d363.png)

