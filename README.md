# demo-single-1rt-statement-timeout
This is a demo with how hack PostgreSQL `statement_timeout` with single round trip

# Описание
Внутри simple query нельзя устанавливать `statement_timeout`:
```
$ psql -U postgres -c "set local statement_timeout = '100ms'; select pg_sleep(2);"
 pg_sleep 
----------
 
(1 row)
```

Это потому, что любой simple query оборачивается в xact_command:
https://github.com/postgres/postgres/blob/REL9_6_STABLE/src/backend/tcop/postgres.c#L923

Если `xact_started == true`, таймер StatementTimeout не взводиться
https://github.com/postgres/postgres/blob/REL9_6_STABLE/src/backend/tcop/postgres.c#L2443

`xact_started = false` устанавливается в 2-х случаях:
- это transcation control statement - BEGIN, ROLLBACK, COMMIT
- это конец query
https://github.com/postgres/postgres/blob/REL9_6_STABLE/src/backend/tcop/postgres.c#L1120-L1141

хак чтобы statement_timeout работал внутри simple query:
```
$ psql -U postgres -c "set local statement_timeout = '100ms'; BEGIN; select pg_sleep(2);"
ERROR:  canceling statement due to statement timeout
```
