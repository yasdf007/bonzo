from apscheduler.triggers.cron import CronTrigger
import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # загружает файл env


connection_string = getenv('DATABASE_URL')

connection = psycopg2.connect(connection_string, sslmode='require')
cursor = connection.cursor()


def scriptexec():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exp (
        username varchar,
        UserID bigint PRIMARY KEY,
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
