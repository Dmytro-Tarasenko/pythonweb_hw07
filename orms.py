from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped
from datetime import date


Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    marks: Mapped[list["Mark"]] = relationship(
        back_populates="student"
    )
    fn_groupid: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(
        back_populates="students"
    )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    students: Mapped[list["Student"]] = relationship(
        back_populates="group"
    )


class Tutor(Base):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="tutor"
    )
    marks: Mapped[list["Mark"]] = relationship(
        back_populates="tutor"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False,
                                      unique=True)
    fn_tutorid: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    marks: Mapped[list["Mark"]] = relationship(
        back_populates="subject"
    )
    tutor: Mapped[Tutor] = relationship(
        back_populates="subjects"
    )


class Mark(Base):
    __tablename__ = "marks_tbl"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[int] = mapped_column(nullable=False)
    recieved: Mapped[date] = mapped_column(nullable=False)
    fn_tutorid: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    fn_studentid: Mapped[int] = mapped_column(ForeignKey("students.id"))
    fn_subjectid: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    student: Mapped[Student] = relationship(back_populates="marks")
    tutor: Mapped[Tutor] = relationship(back_populates="marks")
    subject: Mapped[Subject] = relationship(back_populates="marks")
