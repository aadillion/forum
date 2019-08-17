from .tables import section, post, comment
from aiopg.sa.result import RowProxy
from aiopg.sa import SAConnection as SAConn
from sqlalchemy.sql import literal_column
from datetime import datetime


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

    def __init__(self, theme, description):
        self.theme = theme
        self.description = description

    async def save(self, conn: SAConn):
        await conn.execute(self.table.update().values({self.table.c.theme:self.theme}).where(self.table.c.id == 1))


class Post(Model):
    table = post

    def __init__(self, theme, description, section_id):
        self.theme = theme
        self.description = description
        self.section_id = section_id

    async def save(self, conn: SAConn):
        time = datetime.now()
        await conn.execute(self.table.insert().values(theme=self.theme,
                                                      description=self.description,
                                                      created_at=time,
                                                      modified_at=time))
        return True


class Comment(Model):
    table = comment

    def __init__(self, theme, ):
        self.text = theme


    async def save(self, conn: SAConn):
        time = datetime.now()
        await conn.execute(self.table.insert().values(theme=self.theme,
                                                      description=self.description,
                                                      created_at=time,
                                                      modified_at=time))
        return True

    # @classmethod
    # async def select_all_by_post(cls, conn, post_id):
    #     all_comments = await cls.select_filter_by(conn, {'post_id': post_id})
    #     main_parents = []
    #     for i in all_comments:
    #         pass
    #     # cursor = await co-nn.execute(
    #     #     cls.table.select().where(literal_column(key) == col[key])
    #     # )
    #     # items = await cursor.fetchall()
    #     return 'hello'



