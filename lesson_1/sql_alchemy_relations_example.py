

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship

engine = create_engine('sqlite:///sqlalchemy_example_relations.sqlite')
DBSession = sessionmaker(bind=engine)  # Abstract sessions factory

Base = declarative_base()

class WorkerTeam(Base):
    __tablename__ = 'workersteams'

    id: Mapped[int] = mapped_column(primary_key=True)
    workerid: Mapped[int] = mapped_column(ForeignKey('workers.id'))
    teamid: Mapped[int] = mapped_column(ForeignKey('teams.id'))


class Worker(Base):
    __tablename__ = 'workers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    my_teams: Mapped[list["Team"]] = relationship(
        secondary='workersteams', back_populates='my_workers'
    )


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    my_workers: Mapped[list["Worker"]] = relationship(
        secondary='workersteams', back_populates='my_teams'
    )


def main():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    with DBSession() as session:
        johny = Worker(name="Johny")
        alice = Worker(name="Alice")
        bob = Worker(name="Bob")

        session.add(johny)
        session.add(alice)
        session.add(bob)

        session.commit()

        team_a = Team(name="Team A", my_workers=[johny, alice])
        team_b = Team(name="Team B", my_workers=[bob, alice])

        session.add(team_a)
        session.add(team_b)

        # session.query(Team).delete()
        # session.query(Worker).delete()
        # session.query(WorkerTeam).delete()

        session.commit()

        for team in session.query(Team).all():
            print(f"Team: {team.name}")
            for worker in team.my_workers:
                print(f"\t{worker.name}")

        for worker in session.query(Worker).all():
            print(f"Worker: {worker.name}")
            for team in worker.my_teams:
                print(f"\t{team.name}")


if __name__ == "__main__":
    main()
