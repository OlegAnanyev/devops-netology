#!/usr/bin/env python3

import socket
import os

hostnames = ["drive.google.com", "mail.google.com", "google.com"]

if os.path.exists("ip_check.txt"):
    # если файл уже есть, загрузим из него базу адресов
    f = open("ip_check.txt", "r")
    ip_dict={}

    lines = f.read().split('\n')
    # не совсем понимаю откуда берётся четвёртый элемент, но удалим его
    del lines[-1]

    for line in lines:
        host = line.split(" - ")[0]
        ip = line.split(" - ")[1]
        ip_dict[host] = ip
    f.close()
else:
    # если файла ещё не было, заполним базу адресов пустышками
    ip_dict = {"drive.google.com":"0.0.0.0", "mail.google.com":"0.0.0.0", "google.com":"0.0.0.0"}

output = ""
f = open("ip_check.txt", "w")
for host in hostnames:
    ip = socket.gethostbyname(host)
    output = output + host + ' - ' + ip+"\n"
    if ip_dict[host] == ip:
        print(host + ' - ' + ip)
    else:
        print("[ERROR] " + host + " IP mismatch: " + ip_dict[host] + " " + ip)
f.write(output)
f.close()
