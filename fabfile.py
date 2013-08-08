#!/bin/python
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
from fabric.api import task, env, fastprint
from fabtools.require import postfix
from fabtools.deb import update_index
# Don't remove even though its unused
# noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

# noinspection PyUnresolvedReferences
from fabgis.dropbox import setup_dropbox, setup_dropbox_daemon
from fabgis.django import setup_apache
from fabgis.utilities import update_git_checkout
from fabgis.common import setup_env, show_environment

@task
def deploy():
    """Initialise or update the git clone.

    e.g. to update the server

    fab -H <host> deploy

    """
    # Ensure we have a mailserver setup for our domain
    # Note that you may have problems if you intend to run more than one
    # site from the same server
    setup_env()
    show_environment()
    site_name = 'visual_changelog'
    base_path = os.path.abspath(os.path.join(
        env.fg.home, 'dev', 'python'))
    git_url = 'http://github.com/timlinux/visual_changelog.git'
    repo_alias = 'visual_changelog'
    fastprint('Checking out %s to %s as %s' % (git_url, base_path, repo_alias))
    update_git_checkout(base_path, git_url, repo_alias)
    code_path = os.path.abspath(os.path.join(base_path, repo_alias))
    update_index()
    postfix.server(site_name)
    setup_apache(site_name, code_path=code_path)

