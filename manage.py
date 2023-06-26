import os
from app import create_app, db, bot
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('TEST_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.environ.get('APP_CONFIG') or 'default')
manager = Manager(app, bot)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    """Выполняет модульное тестирование."""
    if coverage and not os.environ.get('TEST_COVERAGE'):
        import sys
        os.environ['TEST_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

if __name__ == '__main__':
    manager.run()