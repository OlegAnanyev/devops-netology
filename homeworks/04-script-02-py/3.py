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
