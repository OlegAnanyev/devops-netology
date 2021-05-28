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
На AWS во free tier мне доступны только инстансы t2.micro, поэтому уменьшим требования к памяти для маcтеров и воркеров в файле kubespray\roles\kubernetes\preinstall\defaults\main.yml:

```yaml
# Minimal memory requirement in MB for safety checks
minimal_node_memory_mb: 900
minimal_master_memory_mb: 900
```

в файле terraform.tfvars опишем требуемую инфраструктуру:
```tf
#Global Vars
aws_cluster_name = "devtest"

#VPC Vars
aws_vpc_cidr_block       = "10.250.192.0/18"
aws_cidr_subnets_private = ["10.250.192.0/20", "10.250.208.0/20"]
aws_cidr_subnets_public  = ["10.250.224.0/20", "10.250.240.0/20"]

#Bastion Host
aws_bastion_size = "t2.micro"


#Kubernetes Cluster

aws_kube_master_num  = 1
aws_kube_master_size = "t2.micro"

aws_etcd_num  = 1
aws_etcd_size = "t2.micro"

aws_kube_worker_num  = 4
aws_kube_worker_size = "t2.micro"

#Settings AWS ELB

aws_elb_api_port                = 6443
k8s_secure_api_port             = 6443
kube_insecure_apiserver_address = "0.0.0.0"

default_tags = {
  #  Env = "devtest"
  #  Product = "kubernetes"
}

inventory_file = "../../../inventory/hosts"
```

в переменные окружения запишем требуемые параметры, сделаем init и apply:
```bash
export TF_VAR_AWS_ACCESS_KEY_ID="AKIAQ[...]BZX4O2"
export TF_VAR_AWS_SECRET_ACCESS_KEY="4LmXzT[...]kB+B1Kr"
export TF_VAR_AWS_SSH_KEY_NAME="my-ssh-key"
export TF_VAR_AWS_DEFAULT_REGION="eu-central-1"
terraform init
terraform apply
```

инфраструктура успешно создана:
![image](https://user-images.githubusercontent.com/32748936/120026606-fbabc680-bffa-11eb-913f-fa2352d2d363.png)

запустим ansible с использованием сгенерированного inventory:
```
ansible-playbook -i kubespray/inventory/hosts kubespray/cluster.yml -e ansible_user=ubuntu -b --become-user=root --flush-cache
```

```
NO MORE HOSTS LEFT *************************************************************************************************************************************************************************************************************

PLAY RECAP *********************************************************************************************************************************************************************************************************************
bastion                    : ok=18   changed=0    unreachable=0    failed=0    skipped=19   rescued=0    ignored=0
ip-10-250-195-116.eu-central-1.compute.internal : ok=335  changed=5    unreachable=0    failed=0    skipped=503  rescued=0    ignored=1
ip-10-250-204-48.eu-central-1.compute.internal : ok=415  changed=12   unreachable=0    failed=0    skipped=683  rescued=0    ignored=1
ip-10-250-207-81.eu-central-1.compute.internal : ok=360  changed=8    unreachable=0    failed=0    skipped=565  rescued=0    ignored=1
ip-10-250-207-99.eu-central-1.compute.internal : ok=151  changed=3    unreachable=0    failed=0    skipped=261  rescued=0    ignored=0
ip-10-250-214-208.eu-central-1.compute.internal : ok=335  changed=5    unreachable=0    failed=0    skipped=503  rescued=0    ignored=1
ip-10-250-223-137.eu-central-1.compute.internal : ok=335  changed=5    unreachable=0    failed=0    skipped=503  rescued=0    ignored=1
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

зайдём через бастион на контрол-плейн и проверим статус кластера:
![image](https://user-images.githubusercontent.com/32748936/120033405-2a7a6a80-c004-11eb-8420-890e99eaa0f6.png)
