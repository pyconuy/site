# -*- coding: utf-8 -*-
from fabric.api import run, sudo, cd, env

env.hosts = ['uy.pycon.org']

project_location = '/opt/pycon.python.org.uy/current/source'


def update():
    with cd(project_location):
        sudo('git pull origin master', user='yoda')
        sudo('supervisorctl restart pycon_python_org_uy_2013')