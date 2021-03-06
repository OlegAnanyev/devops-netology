## Задача 1

Перед выполнением задания ознакомьтесь с документацией по [администрированию MongoDB](https://docs.mongodb.com/manual/administration/).

Пользователь (разработчик) написал в канал поддержки, что у него уже 3 минуты происходит CRUD операция в MongoDB и её 
нужно прервать. 

Вы как инженер поддержки решили произвести данную операцию:
- напишите список операций, которые вы будете производить для остановки запроса пользователя
```
#посмотрим список выполняющихся в данный моменнт операций, выберем opid той, которую хотим завершить
db.currentOp()

#завершим зависшую операцию
db.killOp(<opid of the query to kill>)
```
- предложите вариант решения проблемы с долгими (зависающими) запросами в MongoDB
```
#в прицнипе решать проблему нужно на уровне приложения, работающего с БД,
чтобы некорректных операций не возникало
#но в качестве дополнительного способа стабилизировать работу системы можно
ограничить максимальное время на выполнение операции, например не более 3 минут:
db.collection.find().maxTimeMS(180000)
```

## Задача 2

Перед выполнением задания познакомьтесь с документацией по [Redis latency troobleshooting](https://redis.io/topics/latency).

Вы запустили инстанс Redis для использования совместно с сервисом, который использует механизм TTL. 
Причем отношение количества записанных key-value значений к количеству истёкших значений есть величина постоянная и
увеличивается пропорционально количеству реплик сервиса. 

При масштабировании сервиса до N реплик вы увидели, что:
- сначала рост отношения записанных значений к истекшим
- Redis блокирует операции записи

Как вы думаете, в чем может быть проблема?

```
Я полагаю, что проблема здесь в исчерпании свободной памяти на сервере Redis. Дело в том, что по условию задания,
при увеличении числа запущенных экземпляров нашего сервиса, увеличивается отношение количества записанных key-value
значений к количеству истёкших, а значит скорость роста числа записываемых значений выше, чем скорость роста числа
выбывающих значений. Таким образом в какой-то момент объём хранимых значений, которые ещё не истекли, превышает объём
доступной для Redis памяти, операции malloc() блокирутся и записать больше данных в БД невозможно, пока часть памяти
не освободится. 
По-возможности нужно увеличить значение параметра maxmemory в конфиге Redis, либо разрешить использование виртуальной
памяти (однако это снизит быстродействие сервера). Если же это невозможно, то следует использовать одну из политик,
срабатывающих после достижения лимита доступной памяти:
volatile-lru - удалять ключи с TTL, которые редко используются
volatile-ttl - удалять ключи с TTL, которые скоро истекут
volatile-random - удалять ключи с TTL в случайном порядке
allkeys-lru - удалять ключи с TTL и без TTL, которые редко используются
allkeys-random - удалять с TTL и без TTL в случайном порядке
```
## Задача 3

Перед выполнением задания познакомьтесь с документацией по [Common Mysql errors](https://dev.mysql.com/doc/refman/8.0/en/common-errors.html).

Вы подняли базу данных MySQL для использования в гис-системе. При росте количества записей, в таблицах базы,
пользователи начали жаловаться на ошибки вида:
```python
InterfaceError: (InterfaceError) 2013: Lost connection to MySQL server during query u'SELECT..... '
```

Как вы думаете, почему это начало происходить и как локализовать проблему?

Какие пути решения данной проблемы вы можете предложить?
```
Видимо возникновение проблемы связано с тем, что какая-то из таблиц в БД слишком разрослась
и при обработке запросов к данной БД, включающих все записи, СУБД не успевает ьобработать данный
запрос. Как в первом задании, для начала следует рассмотреть приложение, использующее БД на
предмет оптимизации осуществляемых запросов. Если оптимизировать запросы невозможно, следует
увеличить значение параметра net_read_timeout со стандартных 30 с. до значения, при котором
запросы будут успевать обрабатываться.
Чтобы понять, какая таблица вызывает проблемы, можно использовать такой запрос, он покажет
размер всех таблиц в мегабайтах:
SELECT 
    table_name AS `Table`, 
    round(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` 
FROM information_schema.TABLES 
WHERE table_schema = "$DB_NAME"
    AND table_name = "$TABLE_NAME";
```
## Задача 4

Перед выполнением задания ознакомтесь со статьей [Common PostgreSQL errors](https://www.percona.com/blog/2020/06/05/10-common-postgresql-errors/) из блога Percona.

Вы решили перевезти гис-систему из задачи 3 на PostgreSQL, так как прочитали в документации, что эта СУБД работает с 
большим объемом данных лучше, чем MySQL.

После запуска пользователи начали жаловаться, что СУБД время от времени становится недоступной. В dmesg вы видите, что:

`postmaster invoked oom-killer`

Как вы думаете, что происходит?

Как бы вы решили данную проблему?
```
Как и в задаче №2 здесь мы сталкиваемся с исчерпанием RAM. Рабочий процесс PostgreSQL под
названием postmaster съедает всю доступную память в системе и механизм Out-Of-Memory Killer
завершает его, чтобы предотвратить падение всей системы. Пути решения следующие:
- провести профилирование запросов к БД, чтобы найти самые ресурсоёмкие, попытаться
их оптимизировать
- при необходимости провести шардирование объёмных таблиц в БД
- установить на сервере дополнительную память
- разрешить использование свопа (снизит быстродействие)
- настроить Out-Of-Memory Killer на завершение процесса postmaster в последнюю
очередь (возможно есть что-то, что можно безболезненно убить)
```
