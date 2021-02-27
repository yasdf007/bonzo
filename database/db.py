from apscheduler.triggers.cron import CronTrigger
import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # загружает файл env

BUILD_SQL = './database/build.sql'

connection_string = getenv('DATABASE_URL')

connection = psycopg2.connect(connection_string, sslmode='require')
cursor = connection.cursor()


def commit():
    connection.commit()


def autoSave(sched):
    sched.add_job(commit, CronTrigger(second=0))


def createDB():
    with open(BUILD_SQL, 'r') as query:
        cursor.execute(query.read())
        commit()
