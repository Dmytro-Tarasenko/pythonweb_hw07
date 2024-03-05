"""Creates and fills database with sqlalchemy"""
from sqlalchemy import create_engine, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime, date


engine = create_engine("sqlite:///sqlalchemy.db", echo=True)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    marks: Mapped[list["Mark"]] = relationship(
        secondary="marks", back_populates="stud_id"
    )
    fn_groupid: Mapped[int] = mapped_column(ForeignKey("groups.id"))


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    students: Mapped[list["Student"]] = relationship(
        secondary="students", back_populates="fn_groupid"
    )


class Tutor(Base):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    subjects: Mapped[list["Subject"]] = relationship(
        secondary="subjects", back_populates="fn_tutorid"
    )
    fn_subjectid: Mapped[int] = mapped_column(ForeignKey("subjects.id"))


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    fn_tutorid: Mapped[int] = mapped_column(ForeignKey("tutors.id"))


class Mark(Base):
    __tablename__ = "marks"

    mark: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    recieved: Mapped[date] = mapped_column(nullable=False, primary_key=True)
    fn_tutorid: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    fn_studentid: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    fn_subjectid: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True)
    PrimaryKeyConstraint(name="pk_marks")


def main():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


if __name__ == "__main__":
    main()
