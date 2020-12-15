# Результат выполнения плейбука
```bash
09:02:43 hawk@ubuntu-server playbook ±|master ✗|→ ansible-playbook -i inventory/prod.yml --ask-pass --ask-vault-pass site.yml
SSH password:
Vault password:

PLAY [Print os facts] *************************

TASK [Gathering Facts] *************************
ok: [localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] *************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] *************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP *************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

# Самоконтроль выполненения задания

1. Где расположен файл с `some_fact` из второго пункта задания?
```bash
playbook/group_vars/all/examp.yml
```
2. Какая команда нужна для запуска вашего `playbook` на окружении `test.yml`?
```bash
ansible-playbook -i inventory/test.yml site.yml
```
3. Какой командой можно зашифровать файл?
```bash
ansible-vault encrypt examp.yml
```
4. Какой командой можно расшифровать файл?
```bash
ansible-vault decrypt examp.yml
```
5. Можно ли посмотреть содержимое зашифрованного файла без команды расшифровки файла? Если можно, то как?
```bash
ansible-vault view examp.yml
```
6. Как выглядит команда запуска `playbook`, если переменные зашифрованы?

```bash
ansible-playbook -i inventory/prod.yml --ask-pass --ask-vault-pass site.yml
```
7. Как называется модуль подключения к host на windows?
```bash
winrm
```
8. Приведите полный текст команды для поиска информации в документации ansible для модуля подключений ssh
```bash
ansible-doc -t connection ssh
```
9. Какой параметр из модуля подключения `ssh` необходим для того, чтобы определить пользователя, под которым необходимо совершать подключение?
```bash
remote_user
```
