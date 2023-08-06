# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))


entry_points = [
    "add=pytodos.todo:add",
    "list=pytodos.todo:_list",
    "listall=pytodos.todo:listall",
    "got=pytodos.todo:kill",
    "t=pytodos.todo:test"
]

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name="pytodos",
    version='1.0.15',
    description="a command line lightweight todos tool.",
    long_description=long_description,
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=["pytodos"],
    url="https://github.com/chuanwu/PyToDos.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[
        "click==6.7"
    ],
)
