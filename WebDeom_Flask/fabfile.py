from fabric.api import local, env, run, sudo, cd

env.hosts = 'root@192.168.235.129.'


def test():
    local('python manage.py test')


def setup():
    pass
