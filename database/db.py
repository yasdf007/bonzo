from apscheduler.triggers.cron import CronTrigger
import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # загружает файл env


database = getenv('DB_DATABASENAME')
user = getenv('DB_USERNAME')
password = getenv('DB_PASSWORD')
host = getenv('DB_HOST')
port = getenv('DB_PORT')

connection = psycopg2.connect(host=f'{host}',
                              database=f'{database}', user=f'{user}', password=f'{password}')

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
