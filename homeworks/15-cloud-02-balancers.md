# Домашнее задание к занятию 15.2 "Вычислительные мощности. Балансировщики нагрузки".

Используя конфигурации, выполненные в рамках ДЗ на предыдущем занятии добавить к Production like сети Autoscaling group из 2 EC2-инстансов с  автоматической установкой web-сервера в private домен. Создать приватный домен в Route53, чтобы был доступ из VPN.

## Задание 1. Создать bucket S3 и разместить там файл с картинкой.

- Создать бакет в S3 с произвольным именем (например, имя_студента_дата).
- Положить в бакет файл с картинкой.
- Сделать доступным из VPN используя ACL.

---

## Задание 2. Создать запись в Route53 домен с возможностью определения из VPN.

- Сделать запись в Route53 на приватный домен, указав адрес LB.

---

## Задание 3. Загрузить несколько ЕС2-инстансов с веб-страницей, на которой будет картинка из S3.

- Сделать Launch configurations с использованием bootstrap скрипта с созданием веб-странички на которой будет ссылка на картинку в S3.
- Загрузить 3 ЕС2-инстанса и настроить LB с помощью Autoscaling Group.

## Решение
```tf
/* ===================================   15.1   =============================================== */
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
  region  = var.AWS_REGION
}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "netology-vpc"
  cidr   = "172.31.0.0/16"
  azs    = ["eu-north-1a", "eu-north-1b", "eu-north-1c"]

  tags = {
    Terraform   = "true"
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
  vpc = true
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
    cidr_block     = "0.0.0.0/0"
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
    enabled = false
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

/* ===================================   15.2   =============================================== */

/* ========================== Security groups ========================== */
resource "aws_security_group" "security_group" {
  name   = "security_group"
  vpc_id = module.vpc.vpc_id
  egress {
    protocol    = -1
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_security_group_rule" "ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.security_group.id
}
resource "aws_security_group_rule" "http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.security_group.id
}
/* ========================== S3 ========================== */

resource "aws_s3_bucket" "bucket" {
  bucket = "ananyev-netology-dz"
  acl    = "private"
  versioning {
    enabled = false
  }
  tags = { Name = "S3 bucket" }
}

resource "aws_s3_bucket_object" "img" {
  bucket = "ananyev-netology-dz"
  acl    = "public-read"
  key    = "ava.png"
  source = "ava.png"
}

/* ========================== Route 53 ========================== */

resource "aws_route53_zone" "dns" {
  name = "dns-to-bucket.local"
  vpc {
    vpc_id = module.vpc.vpc_id
  }
}
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.dns.zone_id
  name    = "www.dns-to-bucket.local"
  type    = "CNAME"
  ttl     = "300"
  records = [aws_elb.elb.dns_name]
}

/* ========================== EC2 ========================== */
data "aws_ami" "aws_ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}
data "template_file" "script" {
  template = file("script.tpl")
  vars = {
    url  = data.aws_s3_bucket.bucket.bucket_domain_name
    file = data.aws_s3_bucket_object.img.key
  }
}

resource "aws_launch_configuration" "as_conf" {
  name_prefix                 = "dz-"
  image_id                    = "ami-0ff338189efb7ed37"
  instance_type               = "t3.micro"
  security_groups             = [aws_security_group.security_group.id]
  key_name                    = "main"
  associate_public_ip_address = true
  //bootstrap
  user_data = data.template_file.script.rendered
}

resource "aws_elb" "elb" {
  name    = "elb"
  subnets = [aws_subnet.public.id, aws_subnet.private.id]
  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }
  security_groups             = [aws_security_group.security_group.id]
  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400
  tags = {
    Name = "elb"
  }
}

resource "aws_autoscaling_group" "autoscaling_group" {
  name                 = "autoscaling_group"
  launch_configuration = aws_launch_configuration.as_conf.name
  min_size             = 3
  max_size             = 3
  vpc_zone_identifier  = [aws_subnet.public.id, aws_subnet.public2.id, aws_subnet.public3.id]
  load_balancers       = [aws_elb.elb.id]
}

/* ========================== Outputs ========================== */
output "url" {
  value = data.aws_s3_bucket.bucket.bucket_domain_name
}
output "file" {
  value = data.aws_s3_bucket_object.img.key
}
output "elb_dns_name" {
  value = aws_elb.elb.dns_name
}
```


