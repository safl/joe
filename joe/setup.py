"""
===================
 A couple of notes
===================

* joe is packaged using namespace packages, this is done to provide a minimal set of
  features of joe itself, making it infinitely expandable
* Resources are packaged within the package for access via importlib.resources
* zip-safe=false is used to easily get access to data-files, also, native namespace
  packages do not support it properly
"""
from setuptools import find_namespace_packages, setup

setup(
    name="joe",
    version="1.0.0dev1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/joe/",
    install_requires=[
        "jinja2",
        "paramiko",
        "pytest",
        "pyyaml",
        "scp",
        "setuptools",
    ],
    entry_points={
        "console_scripts": ["joe=joe.cli.cli:main"],
        "pytest11": ["cijoe = joe.pytest_plugin.hooks_and_fixtures"],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.config", "*.preqs"],
    },
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=["joe.*"]),
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
