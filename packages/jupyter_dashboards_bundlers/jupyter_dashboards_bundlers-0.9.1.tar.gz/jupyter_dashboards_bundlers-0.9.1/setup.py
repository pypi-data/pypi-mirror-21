# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from setuptools import setup

# Get location of this file at runtime
HERE = os.path.abspath(os.path.dirname(__file__))

# Eval the version tuple and string from the source
VERSION_NS = {}
with open(os.path.join(HERE, 'dashboards_bundlers/_version.py')) as f:
    exec(f.read(), {}, VERSION_NS)

setup_args = dict(
    name='jupyter_dashboards_bundlers',
    author='Jupyter Development Team',
    author_email='jupyter@googlegroups.com',
    description='Plugins for jupyter_cms to deploy and download notebooks as dashboard apps',
    long_description='''
    This package adds a *Deploy as* and *Download as* menu items for bundling
notebooks created using jupyter_dashboards as standalone web applications.

See `the project README <https://github.com/jupyter-incubator/dashboards_bundlers>`_
for more information.
''',
    url='https://github.com/jupyter-incubator/dashboards_bundlers',
    version=VERSION_NS['__version__'],
    license='BSD',
    platforms=['Jupyter Notebook 5.x'],
    packages=[
        'dashboards_bundlers',
    ],
    include_package_data=True,
    install_requires=[
        'requests>=2.7',
        'notebook>=5.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
