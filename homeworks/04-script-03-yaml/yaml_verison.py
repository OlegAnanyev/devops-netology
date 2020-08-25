#!/usr/bin/env python3

import socket
import os
import yaml

hostnames = ["drive.google.com", "mail.google.com", "google.com"]

if os.path.exists("ip_check.yaml"):
    # если файл уже есть, загрузим из него базу адресов
    f = open("ip_check.yaml", "r")

    ip_dict = yaml.safe_load(f)
    f.close()
else:
    # если файла ещё не было, заполним базу адресов пустышками
    ip_dict = {"drive.google.com": "0.0.0.0", "mail.google.com": "0.0.0.0", "google.com": "0.0.0.0"}

f = open("ip_check.yaml", "w")
for host in hostnames:
    ip = socket.gethostbyname(host)
    if ip_dict[host] == ip:
        print(host + ' - ' + ip)
    else:
        print("[ERROR] " + host + " IP mismatch: " + ip_dict[host] + " " + ip)
        ip_dict[host] = ip
yaml.dump(ip_dict, f)
f.close()
