import momoko
from tornado.ioloop import IOLoop
ioloop = IOLoop.instance()

class myConnection(momoko.Connection):
    def execute(self,
                operation,
                parameters=(),
                cursor_factory=None):
        print(f"round trip! {operation}")
        return super().execute(operation, parameters, cursor_factory)

conn = myConnection(dsn="host=localhost port=5432 dbname=postgres user=postgres password=postgres")
future = conn.connect()
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
future.result()

######################################################
# case 1
sqls = (
    'SET LOCAL statement_timeout = 1500',
    'SELECT pg_sleep(2)',
)

future = conn.transaction(sqls)
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
try:
    cursor = future.result()
    print("it's not timing out")
except:
    print("it's timing out")

######################################################
# case 2
future = conn.execute('SET LOCAL statement_timeout = 1500; SELECT pg_sleep(2)')
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
try:
    cursor = future.result()
    print("it's not timing out")
except:
    print("it's timing out")

######################################################
# case 3
future = conn.execute('SET LOCAL statement_timeout = 1500; BEGIN; SELECT pg_sleep(2)')
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
try:
    cursor = future.result()
    print("it's not timing out")
except:
    print("it's timing out")

