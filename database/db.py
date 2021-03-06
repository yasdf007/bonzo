from os import getenv
from dotenv import load_dotenv

import asyncpg

load_dotenv()  # загружает файл env

BUILD_SQL = './database/build.sql'

connection_string = getenv('DATABASE_URL')


async def createDB(pool):
    with open(BUILD_SQL, 'r') as query:
        await pool.execute(query.read())


async def connectToDB():
    pool = await asyncpg.create_pool(dsn=connection_string, max_inactive_connection_lifetime=180, ssl='require')
    await createDB(pool)
    return pool
