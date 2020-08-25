04-script-03-yaml

1. Корректный по синтаксису JSON-файл должен выглядеть так:
```json
{ "info" : "Sample JSON output from our service\t",
    "elements" :[
        { "name" : "first",
        "type" : "server",
        "ip" : "7175"
        },
        { "name" : "second",
        "type" : "proxy",
        "ip" : "71.78.22.43"
        }
    ]
}
```
2.
JSON-версия:
```python
#!/usr/bin/env python3

import socket
import os
import json

hostnames = ["drive.google.com", "mail.google.com", "google.com"]

if os.path.exists("ip_check.json"):
    # если файл уже есть, загрузим из него базу адресов
    f = open("ip_check.json", "r")
    ip_dict = json.load(f)
    f.close()
else:
    # если файла ещё не было, заполним базу адресов пустышками
    ip_dict = {"drive.google.com": "0.0.0.0", "mail.google.com": "0.0.0.0", "google.com": "0.0.0.0"}

f = open("ip_check.json", "w")
for host in hostnames:
    ip = socket.gethostbyname(host)
    if ip_dict[host] == ip:
        print(host + ' - ' + ip)
    else:
        print("[ERROR] " + host + " IP mismatch: " + ip_dict[host] + " " + ip)
        ip_dict[host] = ip
json.dump(ip_dict, f)
f.close()
```
YAML-версия:
```python
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
```

3*.
```python
#!/usr/bin/env python3

import sys
import yaml
import json


def is_json(myjson):
    try:
        json_object = json.load(myjson)
    except ValueError as e:
        return False
    return True


def is_yaml(myyaml):
    try:
        yaml_object = yaml.safe_load(myyaml)
    except yaml.YAMLError as e:
        return False
    return True


def json_to_yaml(json_file_name):
    j = open(json_file_name, "r")
    yaml_file_name = json_file_name.split(".")[0] + ".yaml"
    y = open(yaml_file_name, "w")
    yaml.dump(json.load(j), y)
    j.close()
    y.close()
    return


def yaml_to_json(yaml_file_name):
    y = open(yaml_file_name, "r")
    json_file_name = yaml_file_name.split(".")[0] + ".json"
    j = open(json_file_name, "w")
    json.dump(yaml.safe_load(y), j)
    y.close()
    j.close()
    return


if len(sys.argv) < 2:
    print("Need file name to convert!")
    exit(-1)

filename = sys.argv[1]
f = open(filename, "r")

if is_json(f):
    print("JSON!")
    json_to_yaml(filename)
elif is_yaml(f):
    print("YAML!")
    yaml_to_json(filename)
else:
    print("This file isn't JSON or YAML!")
    exit(-1)
f.close()
```