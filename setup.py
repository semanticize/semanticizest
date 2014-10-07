#!/usr/bin/env python

from setuptools import setup
import os.path


# Get __version__ from source
dist_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dist_dir, 'semanticizest/_version.py')) as versionpy:
    exec(versionpy.read())


def readme():
    try:
        with open(os.path.join(dist_dir, 'README.rst')) as f:
            return f.read()
    except IOError:
        return ""


def requirements():
    with open(os.path.join(dist_dir, "requirements.txt")) as f:
        return f.readlines()


setup(
    name="semanticizest",
    description="Semanticizer NG",
    long_description=readme(),
    packages=["semanticizest"],
    url="https://github.com/semanticize/semanticizest",
    version=__version__,
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
    ],
    install_requires=requirements(),
    test_suite='nose.collector',
    tests_require=['nose'],
)
