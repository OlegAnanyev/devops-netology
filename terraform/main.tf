# Configure the AWS Provider
provider "aws" {
  region = "eu-north-1"
}

data "aws_ami" "ubuntu" {
  most_recent      = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "netology" {
  // из какого образа создать инстанс
  ami = data.aws_ami.ubuntu.id
  // тип инстанса
  instance_type = "t2.micro"

  // хотим строго 1 ядро
  cpu_core_count = 1
  // и без hyperthreading
  cpu_threads_per_core = 1
  // защита от удаления инстанса по API не требуется
  disable_api_termination = false
  // при завершении работы инстанса не удалять его полностью, а просто останавливать
  instance_initiated_shutdown_behavior = "stop"
  // расширенный мониторинг не требуется
  monitoring = false
  // присвоить инстансу публичный ip-адрес
  associate_public_ip_address = true
  // каким будет внутренний ip нашего инстанса
  private_ip = "172.31.0.5"
  // следить, проходит ли сетевой трафик на инстанс
  source_dest_check = true
  // разрешим инстансу гибернацию
  hibernation = true
  // назначим тэг
  tags = {
    Name = "Hello_Netology"
  }
}

//
data "aws_caller_identity" "current" {}

//регион будет тот же, что задан в провайдере
data "aws_region" "current" {}