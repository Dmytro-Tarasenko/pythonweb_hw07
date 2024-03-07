"""Select queries for the sqlalchemy.db database."""
from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from orms import Student, Group, Tutor, Subject, Mark

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
DBSession = sessionmaker(bind=engine)


def select_1():
    """Select 5 students with the most average marks."""
    with DBSession() as session:
        res = session.query(Student.name,
                            func.round(func.avg(Mark.mark), 2)\
                            .label('avg_mark'))\
            .select_from(Mark).join(Student) \
            .group_by(Student.id).order_by(desc('avg_mark')) \
            .limit(5).all()
        print(res)
        return res


def select_2():
    """Select student who has the biggest average mark in <SUBJECT>.
        SUBJECT = ['Math', 'Data Science', 'HTML+CSS', 'c',
                   'Statistics', 'Python Core', 'Computer Science', 'Algorithms']
    """
    with (DBSession() as session):
        res = session.query(Student.name,
                            Subject.name,
                            func.round(func.avg(Mark.mark), 2) \
                            .label("avg_mark")) \
            .select_from(Mark).join(Student).join(Subject) \
            .where(Subject.name == "Machine Learning") \
            .group_by(Student.id) \
            .order_by(desc("avg_mark")).first()
        print(res)
        return res


def select_3():
    """Select average mark in groups on in <SUBJECT>.
        SUBJECT = ['Math', 'Data Science', 'HTML+CSS', 'c',
                   'Statistics', 'Python Core', 'Computer Science',
                   'Algorithms']
    """
    with (DBSession() as session):
        res = session.query(Group.name,
                            Subject.name,
                            func.round(func.avg(Mark.mark), 2) \
                            .label("avg_mark")) \
            .select_from(Mark).join(Subject).join(Student) \
            .join(Group, Group.id == Student.fn_groupid) \
            .where(Subject.name == "Python Core") \
            .group_by(Group.id).order_by(desc("avg_mark")).all()
        for _ in res:
            print(_)
        return res


def select_4():
    """Select average mark allover database."""
    with DBSession() as session:
        res = session.query(func.round(func.avg(Mark.mark), 2)).first()
        print(res)
        return res


def select_5():
    """Select courses lectured by the <TUTOR>.
        TUTOR = ['Dr. Michael Ortiz', 'Proff. David Deleon',
                 'Proff. Sherri King', 'Ph.D. Dorothy Phillips',
                 'Ph.D. John Thompson']
    """
    with DBSession() as session:
        tutor_orm = session.query(Tutor) \
            .where(Tutor.name == "Proff. Sherri King").first()
        res = [_.name for _ in tutor_orm.subjects]
    print(res)

    return res


def select_6():
    """Select list of students in a <GROUP>.
        GROUP = ['Group-1', 'Group-2', 'Group-3']
    """
    with DBSession() as session:
        group_orm = session.query(Group) \
            .where(Group.name == "Group-2") \
            .first()
        students = [_.name for _ in group_orm.students]
    print(students)

    return students


def select_7():
    """Select marks of students in a <GROUP> and a certain <SUBJECT>.
        SUBJECT = ['Math', 'Data Science', 'HTML+CSS', 'c',
                   'Statistics', 'Python Core', 'Computer Science',
                   'Algorithms']
        GROUP = ['Group-1', 'Group-2', 'Group-3']
    """
    with DBSession() as session:
        res = session.query(Student.name.label("Student"),
                            Subject.name.label("Subject"),
                            Mark.recieved.label("date"),
                            Mark.mark) \
            .select_from(Mark).join(Student).join(Subject) \
            .join(Group, Group.id == Student.fn_groupid) \
            .where(Group.name == "Group-3",
                   Subject.name == "Python Core").all()
        for _ in res:
            print(_)

        return res


def select_8():
    """Select average mark of <TUTOR> and <SUBJECT>.
        SUBJECT = ['Math', 'Data Science', 'HTML+CSS', 'c',
                   'Statistics', 'Python Core', 'Computer Science',
                   'Algorithms']
        TUTOR = ['Dr. Michael Ortiz', 'Proff. David Deleon',
                 'Proff. Sherri King', 'Ph.D. Dorothy Phillips',
                 'Ph.D. John Thompson']
    """
    with (DBSession() as session):
        res = session.query(Tutor.name.label("Tutor"),
                            Subject.name.label("Subject"),
                            func.round(func.avg(Mark.mark), 2)) \
            .select_from(Mark) \
            .join(Tutor, Mark.fn_tutorid == Tutor.id) \
            .join(Subject, Mark.fn_subjectid == Subject.id) \
            .filter(and_(Tutor.name == "Dr. Michael Ortiz",
                         Subject.name == "Computer Science")).first()
        print(res)


def select_9():
    """Select courses of a certain student."""
    with DBSession() as session:
        res = session.query(Subject.name.label("Subject"),
                            Student.name.label("Student")) \
            .select_from(Mark) \
            .join(Student, Mark.fn_studentid == Student.id) \
            .join(Subject, Mark.fn_subjectid == Subject.id) \
            .filter(Student.name == "Melissa Garrett") \
            .group_by(Subject.name).all()
        for _ in res:
            print(_)
        return res


def select_10():
    """Select list of courses that are lectured to a certain <STUDENT>
            by a certain <TUTOR>.
        TUTOR = ['Dr. Michael Ortiz', 'Proff. David Deleon',
                     'Proff. Sherri King', 'Ph.D. Dorothy Phillips',
                     'Ph.D. John Thompson']
    """
    with DBSession() as session:
        res = session.query(Student.name.label("Student"),
                            Tutor.name.label("Tutor"),
                            Subject.name.label("Subject")) \
            .select_from(Mark).join(Student).join(Subject).join(Tutor) \
            .where(and_(Tutor.name == "Dr. Michael Ortiz",
                        Student.name == "Natalie Cruz")) \
            .group_by(Subject.name).all()
        for _ in res:
            print(_)
        return res


def select_aux_1():
    """Select average mark of a certain <STUDENT> by a <TUTOR>.
        TUTOR = ['Dr. Michael Ortiz', 'Proff. David Deleon',
                     'Proff. Sherri King', 'Ph.D. Dorothy Phillips',
                     'Ph.D. John Thompson']
    """
    with DBSession() as session:
        mark = session.query(Tutor.name.label("tutor"),
                             func.round(func.avg(Mark.mark), 2) \
                             .label("avg_mark"),
                             Student.name.label("student")) \
            .select_from(Mark).join(Student).join(Subject) \
            .join(Tutor, Subject.fn_tutorid == Tutor.id) \
            .where(and_(Tutor.name == "Ph.D. John Thompson",
                        Student.name == "Natalie Cruz")) \
            .group_by(Student.name).first()
        print(mark)
        return mark


def select_aux_2():
    """Select marks in <GROUP> on a last class.
        GROUP = ['Group-1', 'Group-2', 'Group-3']
    """
    fields = ['student', 'subject', 'mark', 'group', 'recieved']
    marks = []
    MarkRow = namedtuple("MarkRow", fields)
    with DBSession() as session:
        group_name = "Group-2"
        last_class = session.query(func.max(Mark.recieved)) \
            .select_from(Mark).join(Student) \
            .join(Group, Group.id == Student.fn_groupid) \
            .where(Group.name == group_name) \
            .group_by(Group.name) \
            .scalar()
        print("Last class was on:", last_class)
        marks_orm = session.query(Student.name.label("student"),
                                  Subject.name.label("subject"),
                                  Mark.mark,
                                  Group.name.label("group"),
                                  Mark.recieved) \
            .select_from(Mark).join(Student).join(Subject) \
            .join(Group, Group.id == Student.fn_groupid) \
            .where(and_(Group.name == group_name,
                        Mark.recieved == last_class)).all()
        for _ in marks_orm:
            row = MarkRow(*_)
            marks.append(row)
            print(row)
        return marks


def main():
    # select_1()
    # select_2()
    # select_3()
    # select_4()
    # select_5()
    # select_6()
    # select_7()
    # select_8()
    # select_9()
    # select_10()
    # select_aux_1()
    select_aux_2()


if __name__ == "__main__":
    main()
