# Результат выполнения плейбука
```bash
10:02:39 hawk@ubuntu-server playbook_extra ±|master ✗|→ ./go.sh
d2d877a1dd6e648fcf15ce3f7b507507b89f09948006bc495296ded5eb7cb343
701e2123436f0a7f45f820dba77809247684a849d1606f8b0cb669e53a913d9b
a76657cc978ae093dbd8ffa6b0bc2a674997d47fffb94c58a9918ba54dacdc27

PLAY [Print os facts] ************************************************************************

TASK [Gathering Facts] ************************************************************************
ok: [localhost]
ok: [fedora]
ok: [centos7]
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host ubuntu should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible release will default to
using the discovered platform python for this host. See https://docs.ansible.com/ansible/2.10/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version 2.12. Deprecation
warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [ubuntu]

TASK [Print OS] ************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [fedora] => {
    "msg": "Fedora"
}

TASK [Print fact] ************************************************************************
ok: [localhost] => {
    "msg": "all default fact"
}
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [fedora] => {
    "msg": "fed default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
fedora                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

ubuntu
centos7
fedora

```
