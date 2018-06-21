#!C:\python\flaskbase\Scripts\python.exe
# -*- coding: utf-8 -*-

import os

COV = None
if os.getenv('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Post, Permission, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post,
                Permission=Permission, Comment=Comment)


@manager.command
def test(coverage=False):
    """run the unit tests"""
    print('test...')
    if coverage and not os.getenv('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
        print('set....')

    import unittest
    print('testrunner...')
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
        print('HTML Version: file://%s/index.html' % covdir)
        COV.erase()


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8001)
    print("run")
    manager.run()
