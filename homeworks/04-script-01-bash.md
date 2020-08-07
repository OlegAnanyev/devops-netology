1.  
```bash
	a=1
	b=2
	
	c=a+b
	vagrant@vagrant:~$ echo $c
	a+b
	#потому что не использовали обращение к переменной через $

	d=$a+$b
	vagrant@vagrant:~$ echo $d
	1+2
	#потому что при присвоении значения переменной $d, переменные $a и $b воспринимаются интерпретатором как строковые 

	e=$(($a+$b))
	vagrant@vagrant:~$ echo $e
	3
	#потому что двойные скобки явно указывают, что $a и $b должны использоваться как целочисленные переменные
```
2. В исходном скрипте не хватало скобки и, что важно, не было оператора break. Я бы оптимизировал скрипт таким образом:
```bash
	#!/bin/bash
	while ((1))
		do
			curl http://localhost:80
			if (($? == 0))
			then
				echo "$(date)" "Host is up!" >> curl.log
				break
	
			else
				echo "$(date)" "Host is down!" >> curl.log
			fi
		sleep 5
	done
```	
3.
```bash
#!/bin/bash
for i in {1..5}
do
	echo "Checking #$i..."
	for host in 192.168.0.1 173.194.222.113 87.250.250.242
	do
		curl http://"$host":80 --max-time 5 1>/dev/null  2>/dev/null
		if (($? == 0))
		then
			echo "$(date) $host is UP!" >> 3.log
		else
			echo "$(date) $host is DOWN!" >> 3.log
		fi
	done
done
```
4.
```bash
#!/bin/bash
i=0
while ((1))
do
	echo "Checking #$i..."
	for host in 192.168.0.1 173.194.222.113 87.250.250.242
	do
		curl http://"$host":80 --max-time 5 1>/dev/null  2>/dev/null
		if (($? == 0))
		then
			echo "$(date) $host is UP!" >> curl.log
		else
			echo "$(date) $host is DOWN!" >> error.log
			exit 1
		fi
	done
((i++))
sleep 3
done
```
5*. 
```bash
#Скрипт /devops-netology/.git/hooks/commit-msg
#!/usr/bin/env bash
while read line; do
    # пропускаем строки комментариев
    if [ "${line:0:1}" == "#" ]; then
        continue
    fi
    if [ ${#line} -ge 30 ]; then
        echo "Длина сообщения коммита должна быть не более 30 символов"
        exit 1
    fi
done < "${1}"
commit_regex='^\[04-script-01-bash\]'
error_msg="Сообщение коммита должно начинаться с [04-script-01-bash]"
#если в сообщении коммита нет строки, начинающейся с нужного шаблона
if ! grep -iqE "$commit_regex" "$1"; then
    echo "$error_msg" >&2
    exit 1
fi
exit 0
```
Проверяем:
```bash
$ git commit -m "test hook"
Сообщение коммита должно начинаться с [04-script-01-bash]

$ git commit -m "[04-script-01-bash] test hook but too long one"
Длина сообщения коммита должна быть не более 30 символов

$ git commit -m "[04-script-01-bash] all good"
[master 2d8e382] [04-script-01-bash] all good
 1 file changed, 1 insertion(+), 1 deletion(-)
```
