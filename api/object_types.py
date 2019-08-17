import graphene
from app.models import Section, Post, Comment


class PostType(graphene.ObjectType):
    id = graphene.ID()
    theme = graphene.String()
    description = graphene.String()
    comments = graphene.Field(graphene.String, post_id=graphene.Int())

    async def resolve_comments(self, info):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Comment.select_all_by_post(conn, self.id)


class SectionType(graphene.ObjectType):
    id = graphene.ID()
    theme = graphene.String()
    description = graphene.String()
    posts = graphene.List(PostType, section_id=graphene.Int())

    async def resolve_posts(self, info):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Post.select_filter_by(conn, {'section_id': self.id})


class SectionPaginationType(graphene.ObjectType):
    total_pages = graphene.Int()
    sections = graphene.List(SectionType)

    async def resolve_total_pages(self, info):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            total_number = await Section.count(conn, {})
        return total_number / self['number']

    async def resolve_sections(self, info):
        app = info.context['request'].app
        offset = self['page'] * self['number'] - self['number']
        limit = self['number']
        async with app['db'].acquire() as conn:
            return await Section.select_with_limit_and_offset(conn, {}, limit, offset)