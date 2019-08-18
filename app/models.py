from .tables import section, post, comment
from aiopg.sa.result import RowProxy
from aiopg.sa import SAConnection as SAConn
from sqlalchemy.sql import literal_column
from collections import defaultdict


class Model(object):
    table = None

    async def save(self, conn: SAConn) -> bool:
        attributes = self.__dict__
        await conn.execute(self.table.insert().values(**attributes))
        return True

    @classmethod
    async def update(cls, conn: SAConn, col: dict, col_upd: dict) -> bool:
        key = list(col.keys())[0]
        query = cls.table.update().where(literal_column(key) == col[key]).values(**col_upd)
        await conn.execute(query)
        return True

    @classmethod
    async def delete(cls, conn: SAConn, col: dict) -> bool:
        key = list(col.keys())[0]
        query = cls.table.delete().where(literal_column(key) == col[key])
        await conn.execute(query)
        return True

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
    async def select_with_limit_and_offset(cls, conn: SAConn, col: dict, limit: int, offset: int,
                                           search: str) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.table.select().where(literal_column(key) == col[key]).\
                limit(limit).offset(offset)
        else:
            query = cls.table.select().limit(limit).offset(offset)
        if search:
            query = cls.get_search_query(query, search)
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def count(cls, conn: SAConn, col: dict, search) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.table.select().where(literal_column(key) == col[key])
        else:
            query = cls.table.select()
        if search:
            query = cls.get_search_query(query, search)
        cursor = await conn.execute(query)
        items = cursor.rowcount
        return items

    @classmethod
    def get_search_query(cls, query, search):
        return query


class SearchableModel(object):
    table = None

    @classmethod
    def get_search_query(cls, query, search):
        query = query.where(cls.table.c.theme.contains(search))
        return query


class Section(SearchableModel, Model):
    table = section

    def __init__(self, theme, description):
        self.theme = theme
        self.description = description


class Post(SearchableModel, Model):
    table = post

    def __init__(self, theme, description, section_id):
        self.theme = theme
        self.description = description
        self.section_id = section_id


class Comment(Model):
    table = comment

    def __init__(self, post_id, text, parent_id=None):
        self.text = text
        self.post_id = post_id
        self.parent_id = parent_id

    @classmethod
    async def select_all_by_post(cls, conn, post_id):
        all_comments = await cls.select_filter_by(conn, {'post_id': post_id})
        return cls.get_comments_tree(all_comments)

    @staticmethod
    def get_comments_tree(comments):
        comments_dict = defaultdict(list)
        for i in comments:
            comments_dict[i.parent_id].append(i.id)

        for id_ in comments_dict[None]:
            tree = {}
            print(Comment.get_childs(comments_dict, id_, tree))

        return 'Hello'

    @staticmethod
    def get_childs(comments_dict, id_, tree):
        list_ = comments_dict.get(id_, '')
        if not list_:
            return ''
        z = {}
        for i in list_:
            z = {**z, **{i: Comment.get_childs(comments_dict, i, tree)}}
        return z



