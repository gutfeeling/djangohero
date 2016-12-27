#!/usr/bin/env python

from setuptools import setup

# setup parameters
setup(name = "djangohero",
      version = "0.1.0",
      description = "Deploy a new Django app to Heroku with a one liner",
      long_description = open("README.md").read(),
      author = "Dibya",
      packages = ["djangohero"],
      package_data = {"djangohero" : []},
      include_package_data = True,
      author_email = "dibyachakravorty@gmail.com",
      entry_points={
          "console_scripts": ["djangohero = djangohero.djangohero:main"]}
)
