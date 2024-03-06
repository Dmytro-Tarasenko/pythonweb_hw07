"""Creates and fills database with sqlalchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from faker import Faker
from faker.providers import DynamicProvider, date_time
from random import choice, randint

from orms import Base, Student, Group, Tutor, Subject, Mark

engine = create_engine("sqlite:///sqlalchemy.db", echo=False)
# engine = create_engine("sqlite:///:memory:", echo=False)
DBSession = sessionmaker(bind=engine)


fake = Faker()
dt_fake = date_time.Provider(fake)

# Dynamic provider for the subjects
subjects = ['Math', 'Data Science', 'HTML+CSS', 'Machine Learning',
            'Statistics', 'Python Core', 'Computer Science', 'Algorithms']

# Dynamic provider for the scientific grades
science_grade_provider = DynamicProvider(
    provider_name="science_grade",
    elements=['Dr.', 'Ph.D.', 'Proff.']
)

fake.add_provider(science_grade_provider)


def fake_tutors():
    """Fills the db with faked tutors"""
    seed = int(datetime.now().timestamp())
    Faker.seed(seed=seed)

    with DBSession() as session:
        for _ in range(5):
            grade = fake.science_grade() + " "
            tutor_title = grade + fake.name()
            tutor = Tutor(name=tutor_title)
            session.add(tutor)
        session.commit()


def fake_students():
    """Fills the db with faked students"""
    seed = int(datetime.now().timestamp())
    Faker.seed(seed=seed)

    with DBSession() as session:
        for _ in range(50):
            groupid = choice([1, 2, 3])
            student = Student(name=fake.name(),
                              fn_groupid=groupid)
            session.add(student)
        session.commit()


def fake_groups():
    """Fills the db with faked groups"""
    with DBSession() as session:
        for _ in range(1, 4):
            group = Group(name=f"Group-{_}")
            session.add(group)
        session.commit()


def fake_subjects():
    """Fills the db with faked subjects"""
    with DBSession() as session:
        for _ in range(8):
            subject = Subject(name=subjects[_],
                              fn_tutorid=choice(range(1, 6)))
            session.add(subject)
        session.commit()


def fake_marks():
    """Fills the db with faked marks"""
    seed = int(datetime.now().timestamp())
    Faker.seed(seed=seed)
    recieved = [fake.date_this_year() for _ in range(15)]
    with (DBSession() as session):
        for cur, student in enumerate(session.query(Student).all()):
            print(f"Filling marks for {student.name} {cur + 1}/50", end="\r")
            for _ in range(randint(10, 20)):
                subject_id = choice(range(1, 9))
                tutor_id = (session.query(Subject)
                            .filter_by(id=subject_id)
                            .first().fn_tutorid)
                mark = Mark(mark=randint(1, 5),
                            recieved=choice(recieved),
                            fn_tutorid=tutor_id,
                            fn_studentid=student.id,
                            fn_subjectid=subject_id)
                session.add(mark)
            session.commit()
    print("\nDone.")


def main():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    fake_tutors()
    fake_students()
    fake_groups()
    fake_subjects()
    fake_marks()


if __name__ == "__main__":
    main()
