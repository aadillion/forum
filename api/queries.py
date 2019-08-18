import graphene
from .object_types import SectionPaginationType, PostPaginationType


class Query(graphene.ObjectType):
    section_pagination = graphene.Field(SectionPaginationType, page=graphene.Int(),
                                        number=graphene.Int(), search=graphene.String())
    post_pagination = graphene.Field(PostPaginationType, page=graphene.Int(),
                                     number=graphene.Int(), section_id=graphene.Int(),
                                     search=graphene.String())

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

    # all_sections = graphene.List(SectionType)
    # section = graphene.Field(SectionType, pk=graphene.Int())

    # async def resolve_all_sections(self, info):
    #     app = info.context['request'].app
    #     async with app['db'].acquire() as conn:
    #         return await Section.select_all(conn)
    #
    # async def resolve_section(self, info, pk):
    #     app = info.context['request'].app
    #     async with app['db'].acquire() as conn:
    #         return await Section.select_one(conn, {'id': pk})