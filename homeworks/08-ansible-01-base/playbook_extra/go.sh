#!/bin/bash
docker run --name ubuntu -d pycontribs/ubuntu:latest sleep 60000
docker run --name centos7 -d pycontribs/centos:7 sleep 60000
docker run --name fedora -d pycontribs/fedora:latest sleep 60000
ansible-playbook -i inventory/prod.yml --ask-vault-pass site.yml
docker rm -f ubuntu centos7 fedora
