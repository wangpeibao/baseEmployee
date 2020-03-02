# 启动代码
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from config import config

app = create_app(config["dev"])

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(make_context={"app": app, "db": db}))
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()