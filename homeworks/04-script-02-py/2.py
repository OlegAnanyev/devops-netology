#!/usr/bin/env python3

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
