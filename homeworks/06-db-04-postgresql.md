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

SELECT attname AS column, avg_width as max_avg_size FROM pg_stats WHERE avg_width = (SELECT MAX(avg_width) FROM pg_stats WHERE tablename='orders');
 column | max_avg_size
--------+--------------
 title  |           16
(1 row)
```

# Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

```
CREATE TABLE orders_1 (CHECK (price > 499)) INHERITS orders;
INSERT INTO orders_1 SELECT * FROM orders WHERE price > 499;

CREATE TABLE orders_2 (CHECK (price <= 499)) INHERITS orders;
INSERT INTO orders_2 SELECT * FROM orders WHERE price <= 499;
# не уверен, надо ли очищать основную таблицу (TRUNCATE orders;), т.к. PostgreSQL поддерживает прозрачное шардирование, если установить правила на основную таблицу
```

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?
```
CREATE RULE order_with_price_more_than_499 AS ON INSERT TO orders WHERE (price > 499) DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE order_with_price_less_than_499 AS ON INSERT TO orders WHERE (price <= 499) DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);
```
# Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.
```
#сохраняем таблицу test_database в файл
pg_dump test_database > /var/lib/postgresql/data/test_database_dump.sql
```

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

```
#нужно добавить ключевое слово UNIQUE к нужному столбцу
--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) UNIQUE NOT NULL,
    price integer DEFAULT 0
);
```
