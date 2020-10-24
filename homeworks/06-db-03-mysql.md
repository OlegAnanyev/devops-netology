# Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

В следующих заданиях мы будем продолжать работу с данным контейнером.

```
docker run --name netology-mysql -v /home/hawk/docker/netology-mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=qwerty -d mysql:8
docker exec -it netology-mysql bash
mysql -uroot -pqwerty
mysql> CREATE DATABASE test_db;
mysql -uroot -pqwerty test_db < /var/lib/mysql/test_dump.sql
mysql> \s
--------------
mysql  Ver 8.0.22 for Linux on x86_64 (MySQL Community Server - GPL)

mysql> USE test_db
mysql> SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_db';
+------------+
| TABLE_NAME |
+------------+
| orders     |
+------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM test_db.orders WHERE price > 300;
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0.00 sec)
```

# Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.
```
mysql> CREATE USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test-pass'
WITH MAX_QUERIES_PER_HOUR 100
FAILED_LOGIN_ATTEMPTS 3
PASSWORD EXPIRE INTERVAL 180 DAY 
ATTRIBUTE '{"name": "James", "lastname": "Pretty"}';

mysql> GRANT SELECT ON test_db.* TO 'test'@'localhost';
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER = 'test' AND HOST = 'localhost';
+------+-----------+-----------------------------------------+
| USER | HOST      | ATTRIBUTE                               |
+------+-----------+-----------------------------------------+
| test | localhost | {"name": "James", "lastname": "Pretty"} |
+------+-----------+-----------------------------------------+
1 row in set (0.01 sec)

```
# Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`

```
SET profiling = 1;
mysql> SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> SHOW PROFILES;
Empty set, 1 warning (0.00 sec)

mysql> SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.00 sec)

#сделаем запрос на изменение с текущим движком (InnoDB)
UPDATE orders SET price = 111 WHERE title='War and Peace';
#изменим движок на MyISAM
ALTER TABLE orders ENGINE = MyISAM;
#сделаем запрос на изменение с текущим движком (MyISAM)
UPDATE orders SET price = 222 WHERE title='War and Peace';

#с MyISAM отработало быстрее
mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                   |
+----------+------------+-----------------------------------------------------------------------------------------+
|        4 | 0.01328650 | UPDATE orders SET price = 111 WHERE title='War and Peace'                               |
|        5 | 0.07570275 | ALTER TABLE orders ENGINE = MyISAM                                                      |
|        6 | 0.00555400 | UPDATE orders SET price = 222 WHERE title='War and Peace'                               |
+----------+------------+-----------------------------------------------------------------------------------------+
```
# Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

**/etc/mysql/my.cnf**
```
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/
# То есть в принципе лучше писать кастомные конфиги в /etc/mysql/conf.d/mysql.cnf и они подцепятся оттуда, но укажем прямо тут

#Скорость IO важнее сохранности данных
innodb_flush_log_at_trx_commit = 2
#Нужна компрессия таблиц для экономии места на диске
innodb_file_per_table = 1
#Размер буффера с незакомиченными транзакциями 1 Мб
innodb_log_buffer_size = 1M
#Буффер кеширования 30% от ОЗУ
innodb_buffer_pool_size = 1G
#Размер файла логов операций 100 Мб
innodb_log_file_size = 100M
```
