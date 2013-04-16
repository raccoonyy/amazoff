#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages  # NOQA

requirements = [
    'distribute',
    'Django>=1.5',
    'South>=0.7.6',
    'django-compressor',
]

extras_require = {
    'local': [
        'coverage>=3.6',
        'django-discover-runner>=0.2.2',
        'django-debug-toolbar>=0.9.4',
    ],
    'test': [
        'coverage>=3.6',
        'django-discover-runner>=0.2.2',
    ],
}

dependency_links = []

#: .. seealso:: <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Topic :: Internet :: WWW/HTTP',
]


#: .. seealso::
#:    * <http://docs.python.org/2/distutils/apiref.html#distutils.core.setup>
#:    * <http://packages.python.org/distribute/setuptools.html#new-and-changed-setup-keywords>
setup(
    name='amazoff',
    description='',
    version='0.1',
    license='',
    author='',
    author_email='@',
    url='',
    packages=find_packages('amazoff'),
    package_dir={
        '': 'amazoff',
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    dependency_links=dependency_links,
    classifiers=classifiers,
    cmdclass={
        # If you want to upload this package to PyPI, remove a below line
        'upload': None,
    },
)
