# -*- coding: utf-8 -*-

import os
import shutil
import sys

from pip.download import PipSession
from pip.req import parse_requirements as requirements
from setuptools import setup, Command

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 2:
    from codecs import open


def parse_requirements(f):
    return [str(r.req) for r in requirements(f, session=PipSession())]


class Dist(Command):
    description = 'Generate static files and create dist package'
    user_options = [
        ('clean', 'c', 'clean dist directories before build (default: false)')
    ]
    boolean_options = ['clean']

    def initialize_options(self):
        self.clean = False

    def finalize_options(self):
        pass

    def run(self):
        if self.clean:
            shutil.rmtree('build', ignore_errors=True)
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('health_check.egg-info', ignore_errors=True)

        self.run_command('sdist')
        self.run_command('bdist_wheel')

# Read requirements
_requirements_file = os.path.join(BASE_DIR, 'requirements.txt')
_tests_requirements_file = os.path.join(BASE_DIR, 'tests/requirements.txt')
_REQUIRES = parse_requirements(_requirements_file)
_TESTS_REQUIRES = parse_requirements(_tests_requirements_file)

# Read description
with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    _LONG_DESCRIPTION = f.read()

_CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Object Brokering',
)
_KEYWORDS = ' '.join([
    'python',
    'stream',
    'data',
    'dispatcher',
    'flow',
    'database',
    'cache',
    'celery',
    'producer',
    'consumer',
    'scheduler',
])

setup(
    name='task-dispatcher',
    version='1.2.0',
    description='Library that provides a system to generate tasks producers and consumers with ease.',
    long_description=_LONG_DESCRIPTION,
    author='José Antonio Perdiguero López',
    author_email='perdy.hh@gmail.com',
    maintainer='José Antonio Perdiguero López',
    maintainer_email='perdy.hh@gmail.com',
    url='https://github.com/PeRDy/task-dispatcher',
    download_url='https://github.com/PeRDy/task-dispatcher',
    packages=[
        'task_dispatcher',
    ],
    include_package_data=True,
    install_requires=_REQUIRES,
    tests_require=_TESTS_REQUIRES,
    extras_require={
        'dev': [
            'setuptools',
            'pip',
            'wheel',
            'prospector',
            'twine',
            'bumpversion',
            'pre-commit',
            'nose'
            'tox',
        ]
    },
    license='GPLv3',
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
    test_suite='nose.collector',
    cmdclass={
        'dist': Dist,
    },
    entry_points={
        'console_scripts': [
            'task_dispatcher = task_dispatcher.__main__:main',
        ],
    },
)
