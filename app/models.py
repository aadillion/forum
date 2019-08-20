import json
from collections import defaultdict
from aiopg.sa.result import RowProxy
from aiopg.sa import SAConnection as SAConn
from sqlalchemy.sql import literal_column
from .tables import section, post, comment


class Model(object):
    __table__ = None

    async def save(self, conn: SAConn) -> bool:
        attributes = self.__dict__
        await conn.execute(self.__table__.insert().values(**attributes))
        return True

    @classmethod
    async def update(cls, conn: SAConn, col: dict, col_upd: dict) -> bool:
        key = list(col.keys())[0]
        query = cls.__table__.update().where(literal_column(key) == col[key]).values(**col_upd)
        await conn.execute(query)
        return True

    @classmethod
    async def delete(cls, conn: SAConn, col: dict) -> bool:
        key = list(col.keys())[0]
        query = cls.__table__.delete().where(literal_column(key) == col[key])
        await conn.execute(query)
        return True

    @classmethod
    async def select_one(cls, conn: SAConn, col: dict) -> RowProxy:
        key = list(col.keys())[0]
        query = cls.__table__.select().where(literal_column(key) == col[key])
        cursor = await conn.execute(query)
        item = await cursor.fetchone()
        return item

    @classmethod
    async def select_all(cls, conn: SAConn) -> RowProxy:
        query = cls.__table__.select()
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def select_filter_by(cls, conn: SAConn, col: dict) -> RowProxy:
        key = list(col.keys())[0]
        query = cls.__table__.select().where(literal_column(key) == col[key])
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def select_with_limit_and_offset(cls, conn: SAConn, col: dict, limit: int, offset: int,
                                           search: str) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.__table__.select().where(literal_column(key) == col[key]).\
                limit(limit).offset(offset)
        else:
            query = cls.__table__.select().limit(limit).offset(offset)
        if search:
            query = cls.get_search_query(query, search)
        cursor = await conn.execute(query)
        items = await cursor.fetchall()
        return items

    @classmethod
    async def count(cls, conn: SAConn, col: dict, search) -> RowProxy:
        if col:
            key = list(col.keys())[0]
            query = cls.__table__.select().where(literal_column(key) == col[key])
        else:
            query = cls.__table__.select()
        if search:
            query = cls.get_search_query(query, search)
        cursor = await conn.execute(query)
        items = cursor.rowcount
        return items

    @classmethod
    def get_search_query(cls, query, search):
        return query


class SearchableMixin(object):
    __table__ = None

    @classmethod
    def get_search_query(cls, query, search):
        query = query.where(cls.__table__.c.theme.contains(search))
        return query


class Section(SearchableMixin, Model):
    __table__ = section

    def __init__(self, theme: str, description: str) -> None:
        self.theme = theme
        self.description = description


class Post(SearchableMixin, Model):
    __table__ = post

    def __init__(self, theme: str, description: str, section_id) -> None:
        self.theme = theme
        self.description = description
        self.section_id = section_id


class Comment(Model):
    __table__ = comment

    def __init__(self, post_id: int, text: str, parent_id=None) -> None:
        self.text = text
        self.post_id = post_id
        self.parent_id = parent_id

    @classmethod
    async def select_all_by_post(cls, conn: SAConn, post_id: int) -> json:
        all_comments = await cls.select_filter_by(conn, {'post_id': post_id})
        return cls.get_comments_tree(all_comments)

    @staticmethod
    def get_comments_tree(comments: RowProxy) -> json:
        grouped_comments = Comment.group_comments_by_parent(comments)
        whole_tree = {}
        for i in grouped_comments[None]:
            tree = {}
            whole_tree[i.id] = (i.text, i.created_at.timestamp(),
                                Comment.get_childs(grouped_comments, i.id, tree))

        return json.dumps(whole_tree, default=str)

    @staticmethod
    def group_comments_by_parent(comments: RowProxy) -> defaultdict:
        grouped = defaultdict(list)
        for i in comments:
            grouped[i.parent_id].append(i)
        return grouped

    @staticmethod
    def get_childs(comments_dict: defaultdict, id_: int, tree: dict) -> dict:
        list_ = comments_dict.get(id_, '')
        if not list_:
            return {}
        z = {}
        for i in list_:
            z = {**z, **{i.id: (i.text, i.created_at.timestamp(),
                                Comment.get_childs(comments_dict, i.id, tree))}}
        return z

