from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger

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


def autoSave(sched):
    sched.add_job(commit, CronTrigger(second=0))
