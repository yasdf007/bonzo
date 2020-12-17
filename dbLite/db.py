from sqlite3 import connect

connection = connect('./dbLite/database.sqlite', check_same_thread=False)
cursor = connection.cursor()


def scriptexec():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exp (
        username TEXT,
        UserID integer PRIMARY KEY,
        XP integer DEFAULT 0
        )
        ''')


def execute(command, *values):
    cursor.execute(command,
                   tuple(values))


def commit():
    connection.commit()
