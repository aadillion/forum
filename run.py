from aiohttp import web
import aiohttp_cors
from forum.routes import init_routes
from aiopg.sa import create_engine
from app.tables import section, post, comment
from sqlalchemy.sql.ddl import CreateTable
import sqlalchemy as sa
from config.utils import get_config


def init_config(app: web.Application) -> None:
    app['config'] = get_config()


async def init_pg(app: web.Application) -> None:
    cfg = app['config']['postgres']
    engine = await create_engine(
        database=cfg['database'],
        user=cfg['user'],
        password=cfg['password'],
        host=cfg['host'],
        port=cfg['port'])
    app['db'] = engine


async def close_pg(app: web.Application) -> None:
    app['db'].close()
    await app['db'].wait_closed()


def create_tables(app: web.Application) -> None:
    cfg = app['config']['postgres']
    engine = sa.create_engine(f'postgresql://{cfg["user"]}:{cfg["password"]}@'
                              f'{cfg["host"]}:{cfg["port"]}/{cfg["database"]}')
    try:
        engine.execute(CreateTable(section))
        engine.execute(CreateTable(post))
        engine.execute(CreateTable(comment))
    except Exception as e:
        print(e)


def init_app() -> web.Application:
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    init_config(app)
    init_routes(app, cors)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    create_tables(app)
    return app


web.run_app(init_app(), host='0.0.0.0', port=8080)

