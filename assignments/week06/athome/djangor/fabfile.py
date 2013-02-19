from fabric.api import env, abort, run
from fabric.contrib.project import rsync_project
from fabric.contrib.console import confirm
from fabric.decorators import runs_once
import os.path

env.user = 'week06'
env.webapp_path = '/var/www/sites/week06-djangor/'
env.excluded = ['webroot']
env.local_project_dir = os.path.dirname(env.real_fabfile)


def production():
    env.name = 'production'
    env.hosts = [
        'block647049-vxq.blueboxgrid.com',
    ]


#######################

def deploy(extras=''):
    """
    Deploy code
    """
    if not confirm('Are you sure you want to deploy to ' + env.name + '?', default=False):
        abort('Deployment aborted')

    # upload from local to the server
    rsync(extras)

    # collectstatic
    collectstatic()


def rsync(extras=''):
    """
    Rsync project files
    """
    rsync_project(
        remote_dir=env.webapp_path,
        local_dir="{0}/".format(env.local_project_dir),
        delete=True,
        exclude=env.excluded + ['fabfile.py', '.*', '*.pyc', '*.iml', '*~'],
        extra_opts='--archive --update ' + extras,
    )


@runs_once
def collectstatic():
    """
    Runs collectstatic
    """
    run(env.webapp_path + 'manage.py collectstatic --noinput')


def pip_install(package):
    """
    Installs a python package with pip
    """
    run("pip install {0}".format(package))
