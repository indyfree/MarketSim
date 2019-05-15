#!/usr/bin/env python
from setuptools import setup

setup(
    name="marketsim",
    version="0.0.1",
    packages=find_packages(where="marketsim"),
    package_dir={"": "marketsim"},
    include_package_data=True,
    install_requires=[
        "keras-rl>=0.4.2",
        "gym>=0.2.3",
        "pandas>=0.23.4",
        "tensorflow>=1.13.0",
    ],
)
