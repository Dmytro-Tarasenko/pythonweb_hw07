"""CLI nightmare for CRUD db operations"""
import argparse
from typing import Any, Collection

from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from orms import Student, Subject, Tutor, Group, Mark

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
DBSession = sessionmaker(bind=engine)


def make_ntuple(name: str,
                fields: list[str],
                values: Collection) -> Any:
    if len(fields) != len(values):
        raise IndexError(f"Number of fields {len(fields)} must be equal to"
                         + f" number of values (actually is {len(values)})")
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI provider for basic CRUD operations.",
        epilog="==================================="
    )
    parser.add_argument(
        "-a", "--action", action="store", dest="crud",
        help="defines operation to perform: Create, Show, Update, Delete;"
    )
    parser.add_argument(
        "-m", "--model",
        action="store", dest="model",
        help="define model to operate with: Tutor, Student, Group, Subject;"
    )
    parser.add_argument(
        "-i", "--id",
        action="store", dest="id", default=None,
        help="defines identifier of the record to manipulate;"
    )
    parser.add_argument(
        "-n", "--name",
        action="store", dest="name", default=None,
        help="defines name of the record to manipulate;"
    )
    parser.add_argument(
        "-un", "--update_name",
        action="store", dest="uname", default=None,
        help="defines new name of the record;"
    )
