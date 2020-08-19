04-script-02-py

1.
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

    Какое значение будет присвоено переменной c? -- получим ошибку из-за несоответствия типов
    Как получить для переменной c значение 12? -- a = '1'
    Как получить для переменной c значение 3? -- b = 2

2.
```python
import os

repo_dir = "/home/hawk/PycharmProjects/devops-netology/"
bash_command = ["cd "+repo_dir, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
prepare_result = ""
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = prepare_result + repo_dir + result.replace('\tmodified:   ', '') + "\n"
print(prepare_result)
```
Тест:
```
/home/hawk/PycharmProjects/devops-netology/README.md
/home/hawk/PycharmProjects/devops-netology/homeworks/02-git-04-tools.txt
/home/hawk/PycharmProjects/devops-netology/test1.txt
```
3.
```python
#!/usr/bin/env python3

import os
import sys

# repo_dir = "/home/hawk/PycharmProjects/devops-netology/"
if len(sys.argv) < 2 or os.path.exists(sys.argv[1]) is not True:
    print("Need path to git repository as a parameter!")
    exit(-1)

repo_dir = sys.argv[1]

bash_command = ["cd " + repo_dir, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
prepare_result = ""

if result_os != "" and result_os.find("not a git repository") == -1:
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = prepare_result + repo_dir + result.replace('\tmodified:   ', '') + "\n"
    print(prepare_result)
else:
    print("It's not a git repository!")
    exit(-1)
```
Тест:
```
$./3.py /home/hawk/PycharmProject
Need path to git repository as a parameter!

$./3.py /home/hawk/PycharmProjects/
fatal: not a git repository (or any of the parent directories): .git
It's not a git repository!

$./3.py /home/hawk/PycharmProjects/devops-netology/
/home/hawk/PycharmProjects/devops-netology/README.md
/home/hawk/PycharmProjects/devops-netology/homeworks/02-git-04-tools.txt
/home/hawk/PycharmProjects/devops-netology/test1.txt
```
4.
```python
#!/usr/bin/env python3

import socket
import os

hostnames = ["drive.google.com", "mail.google.com", "google.com"]

if os.path.exists("ip_check.txt"):
    # если файл уже есть, загрузим из него базу адресов
    f = open("ip_check.txt", "r")
    ip_dict={}

    lines = f.read().split('\n')
    # последняя строка пустая, удалим её
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
```
5*.
```python
#!/usr/bin/env python3
import sys
from github import Github
if len(sys.argv) > 1 and sys.argv[1] != "":
    pr_body = sys.argv[1]
else:
    print("Pull request message can't be empty!")
    exit(-1)

repo_name = "devops-netology"
g = Github("###TOKEN###TOKEN###TOKEN###")

repo = g.get_user().get_repo(repo_name)

print("Creating pull request on repo: " + repo_name + ". With message: " + pr_body)
repo.create_pull(title="Pull request from Python script", body=pr_body, head="new_branch", base="master")
```
Тестовый PR: https://github.com/OlegAnanyev/devops-netology/pull/4