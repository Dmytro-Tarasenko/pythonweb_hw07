"""Select queries for the sqlalchemy.db database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orms import Student, Group, Tutor, Subject

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
DBSession = sessionmaker(bind=engine)


def select_1():
    """Select 5 students with the most average marks."""
    pass


def select_2():
    """Select stident who has the most average mark in the subject "Math"."""
    pass


def select_3():
    """Select average mark in groups in the subkect "Math"."""
    pass


def select_4():
    """Select average mark allover database."""
    pass


def select_5():
    """Select courses lectured by the tutor."""
    pass


def select_6():
    """Select list of students in a certain group."""
    pass


def select_7():
    """Select marks of students in a certain group and a certain subject."""
    pass


def select_8():
    """Select average mark of a sertain tutor and a certain subject."""
    pass


def select_9():
    """Select courses of a certain student."""
    pass


def select_10():
    """Select list of courses that are lectured to a certain student by a certain tutor."""
    pass


def select_aux_1():
    """Select average mark of a certain student by a certain tutor."""
    pass


def select_aux_2():
    """Select marks in certain group on a last class."""
    pass


def main():
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()


if __name__ == "__main__":
    main()