import graphene
from .object_types import SectionPaginationType, PostPaginationType, SectionType, PostType
from app.models import Section, Post


class Query(graphene.ObjectType):
    get_section = graphene.Field(SectionType, id_=graphene.Int())
    get_post = graphene.Field(PostType, id_=graphene.Int())
    section_pagination = graphene.Field(SectionPaginationType, page=graphene.Int(),
                                        number=graphene.Int(), search=graphene.String())
    post_pagination = graphene.Field(PostPaginationType, page=graphene.Int(),
                                     number=graphene.Int(), section_id=graphene.Int(),
                                     search=graphene.String())

    async def resolve_get_section(self, info, id_):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Section.select_one(conn, {'id': id_})

    async def resolve_get_post(self, info, id_):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Post.select_one(conn, {'id': id_})

    def resolve_section_pagination(self, info, page, number, **kwargs):
        obj_to_return = dict()
        obj_to_return['page'] = page
        obj_to_return['number'] = number
        obj_to_return['search'] = kwargs.get('search')
        return obj_to_return

    def resolve_post_pagination(self, info, page, number, section_id, **kwargs):
        obj_to_return = dict()
        obj_to_return['page'] = page
        obj_to_return['number'] = number
        obj_to_return['section_id'] = section_id
        obj_to_return['search'] = kwargs.get('search')
        return obj_to_return