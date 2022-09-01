from setuptools import find_namespace_packages, setup

setup(
    name="cijoe-pkg-xnvme",
    version="0.5.0.dev1",
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/refenv/joe-pkg-xnvme/",
    license="BSD",
    install_requires=[
        "cijoe",
        "cijoe-pkg-linux",
        "cijoe-pkg-qemu",
        "cijoe-pkg-fio",
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
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
