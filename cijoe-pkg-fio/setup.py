"""
This is a utility package, that is, contains worklets for building the kernel and
wrappers around kernel features such as null_blk and kmemleak, since it is not tracking
a specific version of the kernel, then the version number tracks the main cijoe package
instead.
"""
from setuptools import find_namespace_packages, setup

setup(
    name="cijoe-pkg-fio",
    version="0.9.0.dev1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/joe-pkg-fio/",
    install_requires=[
        "cijoe",
        "cijoe-pkg-linux",
    ],
    include_package_data=True,
    package_data={
        "": ["*.html", "*.config", "*.perfreq", "*.workflow"],
    },
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=["cijoe.*"]),
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
