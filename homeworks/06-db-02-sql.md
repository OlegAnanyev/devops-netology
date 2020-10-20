# Домашнее задание к занятию "6.2. SQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.
```
docker run -v /home/hawk/docker/netology-postgres/data:/var/lib/postgresql/data -v /home/hawk/docker/netology-postgres/backup:/var/lib/postgresql/backup -e POSTGRES_PASSWORD=mysecretpassword -d postgres:12
```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Приведите:
- итоговый список БД после выполнения пунктов выше,
```
test_db-# \list
                                     List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |       Access privileges
-----------+----------+----------+------------+------------+--------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                  +
           |          |          |            |            | postgres=CTc/postgres         +
           |          |          |            |            | "test-admin-user"=CTc/postgres
(4 rows)
```
- описание таблиц (describe)
```
test_db-# \d orders;
                                   Table "public.orders"
 Column |         Type          | Collation | Nullable |              Default
--------+-----------------------+-----------+----------+------------------------------------
 id     | integer               |           | not null | nextval('orders_id_seq'::regclass)
 name   | character varying(80) |           |          |
 price  | integer               |           |          |
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_order_fkey" FOREIGN KEY ("order") REFERENCES orders(id)

test_db-# \d clients;
                                    Table "public.clients"
  Column  |         Type          | Collation | Nullable |               Default
----------+-----------------------+-----------+----------+-------------------------------------
 id       | integer               |           | not null | nextval('clients_id_seq'::regclass)
 lastname | character varying(80) |           |          |
 country  | character varying(80) |           |          |
 order    | integer               |           |          |
Foreign-key constraints:
    "clients_order_fkey" FOREIGN KEY ("order") REFERENCES orders(id)
```
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
```

```
- список пользователей с правами над таблицами test_db
```
test_db-# \dp orders;
                                     Access privileges
 Schema |  Name  | Type  |        Access privileges         | Column privileges | Policies
--------+--------+-------+----------------------------------+-------------------+----------
 public | orders | table | postgres=arwdDxt/postgres       +|                   |
        |        |       | "test-simple-user"=arwd/postgres |                   |
(1 row)

test_db-# \dp clients;
                                     Access privileges
 Schema |  Name   | Type  |        Access privileges         | Column privileges | Policies
--------+---------+-------+----------------------------------+-------------------+----------
 public | clients | table | postgres=arwdDxt/postgres       +|                   |
        |         |       | "test-simple-user"=arwd/postgres |                   |
(1 row)
```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис - вычислите количество записей в каждой таблице и 
приведите в ответе запрос и получившийся результат.
```
INSERT INTO orders("id", "name", "price") VALUES(1, 'Шоколад', 10);
INSERT INTO orders("id", "name", "price") VALUES(2, 'Принтер', 3000);
INSERT INTO orders("id", "name", "price") VALUES(3, 'Книга', 500);
INSERT INTO orders("id", "name", "price") VALUES(4, 'Монитор', 7000);
INSERT INTO orders("id", "name", "price") VALUES(5, 'Гитара', 4000);

INSERT INTO clients("id", "lastname", "country") VALUES(1, 'Иванов Иван Иванович', 'USA');
INSERT INTO clients("id", "lastname", "country") VALUES(2, 'Петров Петр Петрович', 'Canada');
INSERT INTO clients("id", "lastname", "country") VALUES(3, 'Иоганн Себастьян Бах', 'Japan');
INSERT INTO clients("id", "lastname", "country") VALUES(4, 'Ронни Джеймс Дио', 'Russia');
INSERT INTO clients("id", "lastname", "country") VALUES(5, 'Ritchie Blackmore', 'Russia');

SELECT COUNT(*) FROM orders;
 count
-------
     5
(1 row)

test_db=# SELECT COUNT(*) FROM clients;
 count
-------
     5
(1 row)
```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.
Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
```
UPDATE clients SET "order" = (SELECT id FROM orders WHERE "name"='Книга') WHERE "lastname"='Иванов Иван Иванович';
UPDATE clients SET "order" = (SELECT id FROM orders WHERE "name"='Монитор') WHERE "lastname"='Петров Петр Петрович';
UPDATE clients SET "order" = (SELECT id FROM orders WHERE "name"='Гитара') WHERE "lastname"='Иоганн Себастьян Бах';

SELECT "lastname" FROM clients WHERE "order" IS NOT NULL;
                lastname
----------------------------------------
 Иванов Иван Иванович
 Петров Петр Петрович
 Иоганн Себастьян Бах
(3 rows)
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).
Приведите получившийся результат и объясните что значат полученные значения.
```
EXPLAIN SELECT "lastname" FROM clients WHERE "order" IS NOT NULL;
                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on clients  (cost=0.00..12.00 rows=199 width=178)
   Filter: ("order" IS NOT NULL)
(2 rows)

0.00 -- приблизительная стоимость запуска. Это время, которое проходит, прежде чем начнётся этап вывода данных, например для сортирующего узла это время сортировки.
12.00 -- приблизительная общая стоимость. Она вычисляется в предположении, что узел плана выполняется до конца, то есть возвращает все доступные строки. На практике родительский узел может досрочно прекратить чтение строк дочернего.
199 -- ожидаемое число строк, которое должен вывести этот узел плана. При этом так же предполагается, что узел выполняется до конца.
178 -- ожидаемый средний размер строк, выводимых этим узлом плана (в байтах).
```
## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

```
#делаем дамп базы в каталог для бэкапов
pg_dump test_db > /var/lib/postgresql/backup/test_db.sql

#останавливаем контейнер
docker stop 64a4675b728d

#запускаем новый контейнер с теми же volumes
docker run -v /home/hawk/docker/netology-postgres/data:/var/lib/postgresql/data -v /home/hawk/docker/netology-postgres/backup:/var/lib/postgresql/backup -e POSTGRES_PASSWORD=mysecretpassword -d postgres:12

#логинимся в новый контейнер
docker exec -it 48498ef1ddb0 /bin/bash

#восстанавливаем БД из бэкапа
48498ef1ddb0:/# psql -U postgres -f /var/lib/postgresql/backup/test_db.sql
SET
SET
SET
SET
SET
 set_config
------------

(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
ALTER TABLE
COPY 6
COPY 5
 setval
--------
      1
(1 row)

 setval
--------
      1
(1 row)

ALTER TABLE
ALTER TABLE
GRANT
GRANT
```
