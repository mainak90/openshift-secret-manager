#!/usr/bin/env python
import os
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

packages = ['actions', 'apiclient', 'hvclient', 'logger', 'delete', 'get', 'requeue', 'sync']

package_dir = {
    'actions': 'src/',
    'apiclient': 'src/',
    'hvclient': 'src/',
    'logger': 'src/',
    'delete': 'src/',
    'get': 'src/',
    'requeue': 'src/',
    'sync': 'src/'
}

requires = [
    'openshift==0.9.0',
    'hvac==0.9.6',
    'ruamel.yaml==0.15.97'
]

setup(
    name='openshift-secret-manager',
    version='1.0.0',
    description='Manage Sceret Lifecyles in Openshift',
    author='mdhar',
    author_email='',
    url='https://github.com/mainak90/openshift-secret-manager',
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=requires,
    license='Apache GPL',
    entry_points='''
        [console_scripts]
        feeder=src.app:main
    '''
)