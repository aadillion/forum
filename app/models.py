from .tables import section, post, comment
from aiopg.sa.result import RowProxy
from aiopg.sa import SAConnection as SAConn
from sqlalchemy.sql import literal_column


class Model(object):
    table = None

    @classmethod
    async def select_one(cls, conn: SAConn, col: dict) -> RowProxy:
        key = list(col.keys())[0]
        query = cls.table.select().where(literal_column(key) == col[key])
        cursor = await conn.execute(query)
        item = await cursor.fetchone()
        return item

    @classmethod
    async def select_all(cls, conn: SAConn) -> RowProxy:
        query = cls.table.select()
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def select_filter_by(cls, conn: SAConn, col: dict) -> RowProxy:
        key = list(col.keys())[0]
        query = cls.table.select().where(literal_column(key) == col[key])
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def select_with_limit_and_offset(cls, conn: SAConn, col: dict, limit: int, offset: int) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.table.select().where(literal_column(key) == col[key]).limit(limit).offset(offset)
        else:
            query = cls.table.select().limit(limit).offset(offset)
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def count(cls, conn: SAConn, col: dict) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.table.select().where(literal_column(key) == col[key])
        else:
            query = cls.table.select()
        cursor = await conn.execute(query)
        items = cursor.rowcount
        return items


class Section(Model):
    table = section


class Post(Model):
    table = post


class Comment(Model):
    table = comment

    @classmethod
    async def select_all_by_post(cls, conn, post_id):
        all_comments = await cls.select_filter_by(conn, {'post_id': post_id})
        main_parents = []
        for i in all_comments:
            pass
        # cursor = await co-nn.execute(
        #     cls.table.select().where(literal_column(key) == col[key])
        # )
        # items = await cursor.fetchall()
        return 'hello'



