04-script-02-py

1.
```
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

    Какое значение будет присвоено переменной c? -- получим ошибку из-за несоответствия типов
    Как получить для переменной c значение 12? -- a = '1'
    Как получить для переменной c значение 3? -- b = 2

2.
```
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
```
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
123
5.
123