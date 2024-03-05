import sqlite3

sql_injection = "aa' OR 'yes' = 'yes"

def create_db(conn: sqlite3.Connection):
    sql_request = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY NOT NULL,
        name varchar(255) NOT NULL
    );"""

    try:
        c = conn.cursor()
        c.execute(sql_request)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        c.close()


def update_db(conn: sqlite3.Connection, users: list):
    sql = "INSERT INTO users(id, name) VALUES "
    user_str = ",".join([f"({uid}, '{name}')" for uid, name in enumerate(users)])
    
    cur = conn.cursor()

    try:
        cur.execute(sql + user_str)
        conn.commit()
        print("Users added")
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()


def check_user(conn: sqlite3.Connection, username):
    rows = []
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM users WHERE name = '{username}'")
        # cur.execute(f"SELECT * FROM users WHERE name = :username", {"username": username})
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


if __name__ == "__main__":
    with sqlite3.connect("test.sqlite") as conn:
        create_db(conn)
        update_db(conn, ["Anton", "Dima", "Bob"])

        print("Regular request")
        print(check_user(conn, "Andre"))
      
        print("SQL Injection")
        print(check_user(conn, sql_injection))
