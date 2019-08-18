import sqlalchemy as sa
from datetime import datetime


metadata = sa.MetaData()

section = sa.Table(
    'section', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('theme', sa.String(20), nullable=False),
    sa.Column('description', sa.String(200), nullable=False),
    sa.Column('modified_at', sa.DateTime, onupdate=datetime.now, default=datetime.now),
    sa.Column('created_at', sa.DateTime, default=datetime.now),
)

post = sa.Table(
    'post', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('theme', sa.String(20), nullable=False),
    sa.Column('description', sa.String(200), nullable=False),
    sa.Column('modified_at', sa.DateTime, onupdate=datetime.now, default=datetime.now),
    sa.Column('created_at', sa.DateTime, default=datetime.now),
    sa.Column('section_id', None, sa.ForeignKey('section.id', onupdate="CASCADE", ondelete="CASCADE"))
)

comment = sa.Table(
    'comment', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('text', sa.String(200), nullable=False),
    sa.Column('created_at', sa.DateTime, default=datetime.now),
    sa.Column('post_id', None, sa.ForeignKey('post.id', onupdate="CASCADE", ondelete="CASCADE")),
    sa.Column('parent_id', None, sa.ForeignKey('comment.id', onupdate="CASCADE", ondelete="CASCADE"))
)