from os import getenv
from dotenv import load_dotenv

import asyncpg

load_dotenv()  # загружает файл env

BUILD_SQL = './database/build.sql'

connection_string = \
    f'postgresql://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@{getenv("POSTGRES_IP")}/{getenv("POSTGRES_DB")}'


async def createDB(pool):
    with open(BUILD_SQL, 'r') as query:
        await pool.execute(query.read())


async def connectToDB():
    pool = await asyncpg.create_pool(dsn=connection_string, max_inactive_connection_lifetime=180)
    await createDB(pool)
    return pool
    
async def getPrefixes(pool):
    query = "select server_id, prefix from server_settings where prefix is not null;"
    async with pool.acquire() as con:
        res = await con.fetch(query)
    return res


async def insertPrefix(pool, server_id, prefix):
    query = "insert into server_settings(server_id, prefix) values($1, $2) on conflict (server_id) do update set prefix = $2"
    async with pool.acquire() as con:
        await con.execute(query, server_id, prefix) 