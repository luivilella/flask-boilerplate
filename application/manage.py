from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script import Server
from flask_script import Shell

from app.config import env
from app import create_app
from app import db


app = create_app(env('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)
manager = Manager(app)
dev_server = Server(
    host=env('FLASK_HOST', 'localhost'),
    port=env.int('FLASK_PORT', 5000),
    use_reloader=env.bool('FLASK_AUTO_RELOAD', True),
)


@manager.command
def just_a_test_command():
    print('test command')


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', dev_server)


if __name__ == '__main__':
    manager.run()
