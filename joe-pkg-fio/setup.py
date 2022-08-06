"""
This is a package collecting testcases and auxilary utils for testing xNVMe using joe
"""
from setuptools import find_namespace_packages, setup

setup(
    name="joe-pkg-fio",
    version="0.0.1.dev1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/joe-pkg-fio/",
    install_requires=[
        "joe",
        "joe-pkg-linux",
    ],
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
