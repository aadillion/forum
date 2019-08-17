from aiohttp import web
import aiohttp_cors
from forum.routes import init_routes
from aiopg.sa import create_engine
from app.tables import section, post, comment
from sqlalchemy.sql.ddl import CreateTable, DropTable
import sqlalchemy as sa

# postgresql://test:test@127.0.0.1/aiopg_test
CONN_STRING = 'postgresql://postgres:postgres@localhost:5432/main_db'


async def init_pg(app):
    engine = await create_engine(
        database='main_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def create_tables():
    engine = sa.create_engine(CONN_STRING)
    try:
        engine.execute(CreateTable(section))
        engine.execute(CreateTable(post))
        engine.execute(CreateTable(comment))
    except Exception as e:
        print(e)


def init_app() -> web.Application:
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    init_routes(app, cors)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    create_tables()
    return app


web.run_app(init_app(), host='0.0.0.0', port=8880)

