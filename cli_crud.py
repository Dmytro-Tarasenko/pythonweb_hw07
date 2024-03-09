"""CLI nightmare for CRUD db operations"""
import argparse
from typing import Any, Collection, Callable
from rich.console import Console
from rich.table import Table
from datetime import datetime

from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from orms import Student, Subject, Tutor, Group, Mark

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
DBSession = sessionmaker(bind=engine)

CRUD_HANDLERS = {}

MODELS = {
    "student": Student,
    "subject": Subject,
    "tutor": Tutor,
    "group": Group,
    "mark": Mark
}

ROW_FIELDS = {
    "student": ['id', 'name', 'fn_groupid'],
    "subject": ['id', 'name', 'fn_tutorid'],
    "tutor": ['id', 'name'],
    "group": ['id', 'name'],
    "mark": ['id', 'mark', 'recieved', 'fn_tutorid',
             'fn_studentid', 'fn_subjectid']
}


def register_handler(action: str):
    def factory(handler: Callable):
        global CRUD_HANDLERS
        CRUD_HANDLERS[action] = handler

        def inner():
            pass

        return inner
    return factory


def print_table(data: Collection[Any]):
    table = Table()
    for column in data[0]._fields:
        table.add_column(column, justify="right",
                         min_width=5, max_width=20,
                         overflow="fold")
    for row in data:
        table.add_row(*[str(_) for _ in row])
    console = Console()
    console.print(table)


@register_handler(action="create")
def create(arguments: argparse.Namespace):
    model_name = arguments.model.lower()
    Model = MODELS[model_name]
    name = arguments.name
    if name is None:
        print("Name is obligatory for adding data"
              + f" to {model_name.capitalize()}!")
        return
    if model_name == "mark":
        add_mark(arguments)
        return
    with DBSession() as session:
        res = session.query(Model.name).select_from(Model)\
                .where(Model.name == name).first()
        if res:
            print(f"{name} already exists in {model_name.capitalize()}")
            return
        new_record = Model(name=name)
        session.add(new_record)
        session.commit()
    print(f"{name} added to {model_name.capitalize()}")


def add_mark(arguments: argparse.Namespace):
    mark = arguments.mark
    subject = arguments.subject
    student = arguments.name
    if mark is None or subject is None or student is None:
        print("Mark, subject and student are obligatory for adding mark!")
        return
    with DBSession() as session:
        tutor_id = session.query(Subject.fn_tutorid).select_from(Subject)\
            .where(Subject.name == subject).scalar()
        if tutor_id is None:
            print(f"Subject {subject} does not exist!")
            return
        subject_id = session.query(Subject.id).select_from(Subject)\
            .where(Subject.name == subject).scalar()
        if subject_id is None:
            print(f"Subject {subject} does not exist!")
            return
        student_id = session.query(Student.id).select_from(Student)\
            .where(Student.name == student).scalar()
        if student_id is None:
            print(f"Student {student} does not exist!")
            return
        new_record = Mark(mark=mark,
                          recieved=datetime.now().date(),
                          fn_tutorid=tutor_id,
                          fn_studentid=student_id,
                          fn_subjectid=subject_id)
        session.add(new_record)
        session.commit()
    print(f"Mark {mark} added to {student} for {subject}")


@register_handler(action="show")
def read(arguments: argparse.Namespace):

    model_name = arguments.model.lower()
    Model = MODELS[model_name]
    fields = ROW_FIELDS[model_name]
    Row = namedtuple(model_name.capitalize(), fields)
    name = arguments.name
    id_ = arguments.id
    offset = arguments.offset
    limit = arguments.limit
    result = []

    with DBSession() as session:
        if name:
            response = session.query(Model).filter(Model.name == name).all()
        elif id_:
            response = session.query(Model).filter(Model.id == id_).all()
        else:
            response = session.query(Model).offset(offset).limit(limit).all()
        for _ in response:
            row = Row(*[getattr(_, field) for field in fields])
            result.append(row)
    print_table(result)


@register_handler(action="update")
def update(arguments: argparse.Namespace):
    model_name = arguments.model.lower()
    Model = MODELS[model_name]
    name = arguments.name
    uname = arguments.uname
    id_ = arguments.id

    if model_name == "mark":
        print("Mark cannot be updated!")
        return

    if name is None and id_ is None:
        print("Name or id is obligatory for updating data"
              + f" in {model_name.capitalize()}!")
        return

    with DBSession() as session:
        if name:
            res = session.query(Model.name).select_from(Model)\
                .where(Model.name == name).first()
        else:
            res = session.query(Model.name).select_from(Model)\
                .where(Model.id == id_).first()
        if not res:
            print(f"{name} or {id_} does not exist in"
                  + f" {model_name.capitalize()}!")
            return
        if name:
            session.query(Model).filter(Model.name == name)\
                .update({Model.name: uname})
        else:
            session.query(Model).filter(Model.id == id_)\
                .update({Model.name: uname})
        session.commit()
    print(f"{name} or id={id_} updated to {uname} "
          + f"in {model_name.capitalize()}")


@register_handler(action="delete")
def delete(arguments: argparse.Namespace):
    model_name = arguments.model.lower()
    Model = MODELS[model_name]
    name = arguments.name
    id_ = arguments.id
    if name is None and id_ is None:
        print("Name or id is obligatory for deleting data"
              + f" from {model_name.capitalize()}!")
        return
    with DBSession() as session:
        if name:
            res = session.query(Model.name).select_from(Model)\
                .where(Model.name == name).first()
        else:
            res = session.query(Model.name).select_from(Model)\
                .where(Model.id == id_).first()
        if not res:
            print(f"{name} or {id_} does not exist in"
                  + f" {model_name.capitalize()}!")
            return
        if name:
            session.query(Model).filter(Model.name == name).delete()
        else:
            session.query(Model).filter(Model.id == id_).delete()
        session.commit()
    print(f"{name} deleted from {model_name.capitalize()}")


def dispatch(arguments: argparse.Namespace):
    action = arguments.crud.lower()
    CRUD_HANDLERS[action](arguments)


def is_enough_param(arguments: argparse.Namespace) -> bool:
    if arguments.crud is None or arguments.model is None:
        return False
    actions = ["create", "show", "update", "delete"]
    models = ["tutor", "student", "group", "subject", "mark"]
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
              + " Group, Subject, Mark;")
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
                              + " course (-c, --course).)"))
    parser.add_argument("-c", "--course",
                        action="store", dest="subject", default=None,
                        help="course name")

    args = parser.parse_args()
    if not is_enough_param(args):
        parser.print_help()
    else:
        dispatch(args)
