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

resource "aws_nat_gateway" "NAT_for_private_subnet" {
  connectivity_type = "private"
  subnet_id     = aws_subnet.public.id
  depends_on = [aws_internet_gateway.gw]
  
  tags = {
    Name = "NAT for private subnet"
  }
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

/*
resource "aws_ec2_client_vpn_endpoint" "my_vpn_endpoint" {
  description            = "VPN endpont"
  server_certificate_arn = "arn:aws:acm:eu-north-1:016202594952:certificate/f9450162-558c-403f-a600-6be21145edc3" // aws_acm_certificate.cert.arn
  client_cidr_block      = "10.0.0.0/22"

  authentication_options {
    type                       = "certificate-authentication"
    root_certificate_chain_arn = "arn:aws:acm:eu-north-1:016202594952:certificate/f9450162-558c-403f-a600-6be21145edc3" // aws_acm_certificate.root_cert.arn
  }

  connection_log_options {
    enabled               = false
    //cloudwatch_log_group  = aws_cloudwatch_log_group.lg.name
    //cloudwatch_log_stream = aws_cloudwatch_log_stream.ls.name
  }
}
*/
```

Создадим VPN:
![image](https://user-images.githubusercontent.com/32748936/128720926-dc2973fe-46ea-4c88-8ead-8c2e0e9a9b75.png)

Импортируем сертификаты сервера и клиента для VPN на AWS:
```
[hawk:~/custom_folder] 254 $ aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt
{
    "CertificateArn": "arn:aws:acm:eu-north-1:016202594952:certificate/f9450162-558c-403f-a600-6be21145edc3"
}
[hawk:~/custom_folder] $ aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt
{
    "CertificateArn": "arn:aws:acm:eu-north-1:016202594952:certificate/12f191a9-47d7-496d-856c-89b5211a772e"
}
```

Подключимся к VPN:
![image](https://user-images.githubusercontent.com/32748936/128720726-11b83dec-fd93-4d0b-b482-2c7702b1ff14.png)

Подключимся к инстансу в приватной сети по серому IP и проверим доступ в интернет с него:
```bash
ubuntu@ip-172-31-104-28:~$ ping netology.ru
PING netology.ru (172.67.43.83) 56(84) bytes of data.
64 bytes from 172.67.43.83 (172.67.43.83): icmp_seq=1 ttl=51 time=11.4 ms
64 bytes from 172.67.43.83 (172.67.43.83): icmp_seq=2 ttl=51 time=4.30 ms
64 bytes from 172.67.43.83 (172.67.43.83): icmp_seq=3 ttl=51 time=4.25 ms
64 bytes from 172.67.43.83 (172.67.43.83): icmp_seq=4 ttl=51 time=4.34 ms
64 bytes from 172.67.43.83 (172.67.43.83): icmp_seq=5 ttl=51 time=4.24 ms
^C
--- netology.ru ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 4.244/5.708/11.413/2.852 ms
```

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
