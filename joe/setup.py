"""
===================
 A couple of notes
===================

* joe is packaged using namespace packages, this is done to provide a minimal set of
  features of joe itself, making it infinitely expandable
* zip-safe=false is used to easily get access to data-files, also, native namespace
  packages do not support it properly


"""
import glob
import os

from setuptools import find_namespace_packages, setup

setup(
    name="joe",
    version="0.0.1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/joe/",
    install_requires=[
        "jinja2",
        "paramiko",
        "pytest",
        "pyyaml",
        "scp",
    ],
    data_files=[
        ("share/joe/envs", glob.glob(os.path.join("envs", "*"))),
        ("share/joe/templates", glob.glob(os.path.join("templates", "*html"))),
    ],
    entry_points={
        "console_scripts": ["joe=joe.cli.cli:main"],
        "pytest11": ["cijoe = joe.pytest_plugin.hooks_and_fixtures"],
    },
    packages=find_namespace_packages(include=["joe.*"]),
    zip_safe=False,
    options={"bdist_wheel": {"universal": True}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
