from sqlalchemy import create_engine


if __name__ == "__main__":
    engine = create_engine('sqlite:///my_database.sqlite3', echo=True)
    engine.connect()
