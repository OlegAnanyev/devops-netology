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
    cidr_block = aws_subnet.public.cidr_block
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public to the internet"
  }
}

/* ========================== PRIVATE ========================== */
resource "aws_subnet" "private" {
  vpc_id     = module.vpc.vpc_id
  cidr_block = "172.31.96.0/19"

  tags = {
    Name = "private"
  }
}
```

Импортируем сертификаты сервера и клиента для VPN:
```
[hawk:~/custom_folder] $ aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt

An error occurred (AccessDeniedException) when calling the ImportCertificate operation: User: arn:aws:iam::016202594952:user/netology_terraform is not authorized to perform: acm:ImportCertificate on resource: arn:aws:acm:eu-north-1:016202594952:certificate/*
[hawk:~/custom_folder] 254 $ aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt
{
    "CertificateArn": "arn:aws:acm:eu-north-1:016202594952:certificate/f9450162-558c-403f-a600-6be21145edc3"
}
[hawk:~/custom_folder] $ aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt
{
    "CertificateArn": "arn:aws:acm:eu-north-1:016202594952:certificate/12f191a9-47d7-496d-856c-89b5211a772e"
}
```
