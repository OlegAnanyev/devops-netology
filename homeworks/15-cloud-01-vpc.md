# Домашнее задание к занятию "15.1. Организация сети"

Настроить Production like сеть в рамках одной зоны с помощью terraform. Модуль VPC умеет автоматически делать все что есть в этом задании. Но мы воспользуемся более низкоуровневыми абстракциями, чтобы понять, как оно устроено внутри.

1. Создать VPC.

- Используя vpc-модуль terraform, создать пустую VPC с подсетью 172.31.0.0/16.
- Выбрать регион и зону.

2. Публичная сеть.

- Создать в vpc subnet с названием public, сетью 172.31.32.0/19 и Internet gateway.
- Добавить RouteTable, направляющий весь исходящий трафик в Internet gateway.
- Создать в этой приватной сети виртуалку с публичным IP и подключиться к ней, убедиться что есть доступ к интернету.

3. Приватная сеть.

- Создать в vpc subnet с названием private, сетью 172.31.96.0/19.
- Добавить NAT gateway в public subnet.
- Добавить Route, направляющий весь исходящий трафик private сети в NAT.

4. VPN.

- Настроить VPN, соединить его с сетью private.
- Создать себе учетную запись и подключиться через нее.
- Создать виртуалку в приватной сети.
- Подключиться к ней по SSH по приватному IP и убедиться, что с виртуалки есть выход в интернет.

Документация по AWS-ресурсам:

- [Getting started with Client VPN](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-getting-started.html)

Модули terraform

- [VPC](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc)
- [Subnet](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet)
- [Internet Gateway](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway)


# Решение
```tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}
variable "AWS_REGION" {    
    default = "eu-north-1"
}
provider "aws" {
  profile = "default"
  region  = "${var.AWS_REGION}"
}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "netology-vpc"
  cidr = "172.31.0.0/16"
  azs = ["eu-north-1a", "eu-north-1b", "eu-north-1c"]

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}

/* ========================== PUBLIC ========================== */
resource "aws_subnet" "public" {
  vpc_id     = module.vpc.vpc_id
  cidr_block = "172.31.32.0/19"

  tags = {
    Name = "public"
  }
}
resource "aws_internet_gateway" "gw" {
  vpc_id = module.vpc.vpc_id

  tags = {
    Name = "internet gateway"
  }
}

resource "aws_route_table" "pub_to_inet" {
  vpc_id = module.vpc.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public to the internet"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.pub_to_inet.id
}

/* ========================== PRIVATE ========================== */
resource "aws_subnet" "private" {
  vpc_id     = module.vpc.vpc_id
  cidr_block = "172.31.96.0/19"

  tags = {
    Name = "private"
  }
}

resource "aws_eip" "ip_for_nat" {
  vpc      = true
}

resource "aws_nat_gateway" "NAT_for_private_subnet" {
  allocation_id = aws_eip.ip_for_nat.id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "NAT for private subnet"
  }
  depends_on = [aws_internet_gateway.gw]
}


resource "aws_route_table" "private_to_nat" {
  vpc_id = module.vpc.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.NAT_for_private_subnet.id
  }

  tags = {
    Name = "private to the NAT"
  }
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private_to_nat.id
}


/* ========================== VPN ========================== */

resource "aws_ec2_client_vpn_endpoint" "my_vpn_endpoint" {
  description            = "terraform-clientvpn-endpoint"
  server_certificate_arn = "arn:aws:acm:eu-north-1:016202594952:certificate/f9450162-558c-403f-a600-6be21145edc3"
  client_cidr_block      = "10.0.0.0/16"

  authentication_options {
    type                       = "certificate-authentication"
    root_certificate_chain_arn = "arn:aws:acm:eu-north-1:016202594952:certificate/12f191a9-47d7-496d-856c-89b5211a772e"
  }

  connection_log_options {
    enabled               = false
  }
}

resource "aws_ec2_client_vpn_network_association" "vpn_to_private__association" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.my_vpn_endpoint.id
  subnet_id              = aws_subnet.private.id
}

resource "aws_ec2_client_vpn_authorization_rule" "default_vpn_authorization_rule" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.my_vpn_endpoint.id
  target_network_cidr    = aws_subnet.private.cidr_block
  authorize_all_groups   = true
}
```

Подключимся к VPN:
![image](https://user-images.githubusercontent.com/32748936/128720726-11b83dec-fd93-4d0b-b482-2c7702b1ff14.png)


Подключимся к инстансу в публичной сети по белому IP и проверим доступ к интернету:
```bash
ubuntu@ip-172-31-37-78:~$ ping ya.ru
PING ya.ru (87.250.250.242) 56(84) bytes of data.
64 bytes from ya.ru (87.250.250.242): icmp_seq=1 ttl=44 time=47.6 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=2 ttl=44 time=47.6 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=3 ttl=44 time=47.7 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=4 ttl=44 time=47.7 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=5 ttl=44 time=47.7 ms
^C
--- ya.ru ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4007ms
rtt min/avg/max/mdev = 47.569/47.640/47.679/0.038 ms
ubuntu@ip-172-31-37-78:~$
```

Подключимся к инстансу в приватной сети по серому IP и проверим доступ в интернет с него:
```bash
ubuntu@ip-172-31-111-149:~$ ping ya.ru
PING ya.ru (87.250.250.242) 56(84) bytes of data.
64 bytes from ya.ru (87.250.250.242): icmp_seq=1 ttl=43 time=48.9 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=2 ttl=43 time=48.7 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=3 ttl=43 time=48.7 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=4 ttl=43 time=48.7 ms
64 bytes from ya.ru (87.250.250.242): icmp_seq=5 ttl=43 time=48.7 ms
^C
--- ya.ru ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4007ms
rtt min/avg/max/mdev = 48.658/48.731/48.877/0.076 ms
ubuntu@ip-172-31-111-149:~$
```
