# 启动代码
from flask import current_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import get_debug_queries

from app import create_app, db
from config import config

app = create_app(config["dev"])

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(make_context={"app": app, "db": db}))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    pass

# debug模式下的
@app.after_request
def get_query_state(response):
    if current_app.config["DEBUG"]:
        queries = get_debug_queries()
        count = 0
        duration = 0
        for q in queries:
            count += 1
            duration += q.duration
        print("查询次数:%d 耗时:%f ms" % (count, duration * 1000))
    return response

if __name__ == "__main__":
    manager.run()