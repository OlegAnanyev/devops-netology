# Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:

```
#- вывода списка БД
  \l[+]   [PATTERN]      list databases
  
#- подключения к БД  
  \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}
  
#- вывода списка таблиц  
  \d[S+]                 list tables, views, and sequences
  
#- вывода описания содержимого таблиц  
  \d+ to view the Description column for the placenames table
  
#- выхода из psql  
  \q                     quit psql
```
# Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats) столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

```
CREATE DATABASE "test_database";
root@dc4e10998b51:/# psql -U postgres -d test_database < /var/lib/postgresql/data/test_dump.sql
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
ALTER TABLE
COPY 8
 setval
--------
      8
(1 row)



postgres=# \c test_database
You are now connected to database "test_database" as user "postgres".

ANALYZE orders;

#лучшее, что у меня получилось ниже, однако автоматически выбрать столбец с наибольшим значением я не смог

SELECT attname AS column, MAX(avg_width) AS max_avg_size FROM pg_stats WHERE tablename='orders' GROUP BY attname;
 column | max_avg_size
--------+--------------
 id     |            4
 price  |            4
 title  |           16 <----
(3 rows)
```

# Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

# Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?
