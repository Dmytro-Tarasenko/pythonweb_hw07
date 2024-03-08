"""CLI nightmare for CRUD db operations"""
import argparse
from typing import Any, Collection, Callable

from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from orms import Student, Subject, Tutor, Group, Mark

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
DBSession = sessionmaker(bind=engine)

CRUD_HANDLERS = {}


def register_handler(action: str):
    def factory(handler: Callable):
        global CRUD_HANDLERS
        CRUD_HANDLERS[action] = handler

        def inner():
            pass

        return inner
    return factory


def make_namedtuple(fields: list[str],
                    values: Collection,
                    name: str = "ResultRow") -> Any:
    if len(fields) != len(values):
        raise ValueError(f"Number of fields {len(fields)} must be equal to"
                         + f" number of values (actually is {len(values)})")
    cls = namedtuple(name, fields)
    return cls(*values)


@register_handler(action="create")
def create(arguments: argparse.Namespace):
    model = arguments.model.lower().capitalize()
    name = arguments.name
    if name is None:
        print(f"Name is obligatory for adding data to {model}!")
        return
    with DBSession() as session:
        res = session.query(name)


@register_handler(action="show")
def read():
    pass


@register_handler(action="update")
def update():
    pass


@register_handler(action="delete")
def delete():
    pass


def dispatch(arguments: argparse.Namespace):
    action = arguments.crud.lower()
    CRUD_HANDLERS[action](arguments)


def is_enough_param(arguments: argparse.Namespace) -> bool:
    if arguments.crud is None or arguments.model is None:
        return False
    actions = ["create", "show", "update", "delete"]
    models = ["tutor", "student", "group", "subject", "marks"]
    return arguments.crud.lower() in actions and \
        arguments.model.lower() in models


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI provider for basic CRUD operations.",
        epilog="==================================="
    )
    parser.add_argument(
        "-a", "--action", action="store",
        dest="crud", default=None,
        help="defines operation to perform: Create, Show, Update, Delete;"
    )
    parser.add_argument("-o", "--offset",
                        action="store", dest="offset", default=0,
                        help="defines offset in table for Show action;")
    parser.add_argument("-l", "--limit",
                        action="store", dest="limit", default=-1,
                        help="defines limit of table rows to display;")
    parser.add_argument(
        "-m", "--model",
        action="store", dest="model", default=None,
        help=("define model to operate with: Tutor, Student,"
              + " Group, Subject, Marks;")
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
    parser.add_argument("-s", "--score",
                        action="store", dest="mark", default=None,
                        help=("mark scored by student (have to be coupled with"
                              + " student (-n, --name) and"
                              + " subject (-s, --subject).)"))

    args = parser.parse_args()
    if not is_enough_param(args):
        parser.print_help()
    else:
        dispatch(args)
