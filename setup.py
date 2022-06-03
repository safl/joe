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
        ("bin", glob.glob(os.path.join("bin", "*"))),
        ("share/joe/aux", glob.glob(os.path.join("aux", "*"))),
        ("share/joe/envs", glob.glob(os.path.join("envs", "*"))),
        ("share/joe/templates", glob.glob(os.path.join("templates", "*html"))),
    ],
    packages=find_namespace_packages(include=["joe.*"]),
    zip_safe=False,
    options={"bdist_wheel": {"universal": True}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
    ],
)
