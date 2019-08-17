import sqlalchemy as sa


metadata = sa.MetaData()

section = sa.Table(
    'section', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('theme', sa.String(20), nullable=False),
    sa.Column('description', sa.String(200), nullable=False),
    sa.Column('modified_at', sa.DateTime, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
)

post = sa.Table(
    'post', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('theme', sa.String(20), nullable=False),
    sa.Column('description', sa.String(200), nullable=False),
    sa.Column('modified_at', sa.DateTime, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('section_id', None, sa.ForeignKey('section.id'))
)

comment = sa.Table(
    'comment', metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('text', sa.String(200), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('post_id', None, sa.ForeignKey('section.id')),
    sa.Column('parent_id', None, sa.ForeignKey('section.id'))
)