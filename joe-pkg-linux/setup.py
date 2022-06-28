"""
    CIJOE package for Linux
"""
import glob
import os

from setuptools import find_namespace_packages, setup

setup(
    name="joe-pkg-linux",
    version="0.0.1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/joe-pkg-linux/",
    install_requires=[
        "joe",
    ],
    data_files=[
        ("share/joe/envs", glob.glob(os.path.join("envs", "*"))),
    ],
    package_dir={'': 'src'},
    packages=find_namespace_packages(where="src", include=["joe.*"]),
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
