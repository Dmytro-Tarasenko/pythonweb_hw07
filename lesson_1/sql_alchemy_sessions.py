from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship

engine = create_engine('sqlite:///sqlalchemy_example.sqlite')
DBSession = sessionmaker(bind=engine) # Abstract sessions factory

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    street_name: Mapped[str]
    street_number: Mapped[str | None]
    post_code: Mapped[str] = mapped_column(String(250))
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id'))
    person: Mapped["Person"] = relationship()


def main():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    with DBSession() as session:
        new_person = Person(name="Bill")

        session.add(new_person)

        session.commit()

        new_address = Address(
            street_name="IDK", post_code='00000', person=new_person
        )

        session.add(new_address)

        # session.query(Person).delete()
        # session.query(Address).delete()

        session.commit()

        for person in session.query(Person).all():
            print(person.name)

        for address in session.query(Address).all():
            print(f"{address.street_name} {address.person.name}")


if __name__ == "__main__":
    main()