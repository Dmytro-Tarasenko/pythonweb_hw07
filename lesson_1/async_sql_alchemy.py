import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import ForeignKey, select, delete
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

engine = create_async_engine('sqlite+aiosqlite:///sqlalchemy_example_relations.sqlite')
DBSession = async_sessionmaker(bind=engine) # Abstract sessions factory

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
    teams: Mapped[list["Team"]] = relationship(
        secondary='workersteams', back_populates='workers'
    )


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    workers: Mapped[list["Worker"]] = relationship(
        secondary='workersteams', back_populates='teams'
    )


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBSession() as session:
        johny = Worker(name="Johny")
        alice = Worker(name="Alice")
        bob = Worker(name="Bob")

        session.add(johny)
        session.add(alice)
        session.add(bob)

        await session.commit()

        team_a = Team(name="Team A", workers=[johny, alice])
        team_b = Team(name="Team B", workers=[bob, alice])

        session.add(team_a)
        session.add(team_b)

        # await session.execute(delete(Team))
        # await session.execute(delete(Worker))
        # await session.execute(delete(WorkerTeam))

        await session.commit()

        teams = await session.execute(select(Team).options(
            selectinload(Team.workers)
        ))

        for team in teams.scalars():
            print(f"Team: {team.name}")
            for worker in team.workers:
                print(f"\t{worker.name}")

        workers = await session.execute(select(Worker).options(
            selectinload(Worker.teams)
        ))

        for worker in workers.scalars():
            print(f"Worked: {worker.name}")
            for team in worker.teams:
                print(f"\t{team.name}")


if __name__ == "__main__":
    asyncio.run(main())
