"""CLI nightmare for CRUD db operations"""
import argparse
from typing import Iterable, Any

from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from orms import Student, Subject, Tutor, Group, Mark


def make_ntuple(name: str,
                fields: list[str],
                values: Iterable) -> Any:
    cls = namedtuple(name, fields)
    return cls(*values)


def create():
    pass


def read():
    pass


def update():
    pass


def delete():
    pass


