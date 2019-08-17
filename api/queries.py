import graphene
from app.models import Section
from .object_types import SectionPaginationType, SectionType


class Query(graphene.ObjectType):
    section_pagination = graphene.Field(SectionPaginationType, page=graphene.Int(), number=graphene.Int())
    all_sections = graphene.List(SectionType)
    section = graphene.Field(SectionType, pk=graphene.Int())

    def resolve_section_pagination(self, info, page, number):
        obj_to_return = dict()
        obj_to_return['page'] = page
        obj_to_return['number'] = number
        return obj_to_return

    async def resolve_all_sections(self, info):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Section.select_all(conn)

    async def resolve_section(self, info, pk):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            return await Section.select_one(conn, {'id': pk})

