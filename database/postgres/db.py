from os import getenv
from dotenv import load_dotenv

import asyncpg

load_dotenv()  # загружает файл env

BUILD_SQL = 'build.sql'

connection_string = \
    f'postgresql://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@{getenv("POSTGRES_IP")}/{getenv("POSTGRES_DB")}'


async def createDB(pool):
    with open(BUILD_SQL, 'r') as query:
        await pool.execute(query.read())


async def connectToDB():
    pool = await asyncpg.create_pool(dsn=connection_string, max_inactive_connection_lifetime=180)
    await createDB(pool)
    return pool
