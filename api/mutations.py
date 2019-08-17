import graphene
from graphql import ResolveInfo
from app.models import Section, Post, Comment
from .object_types import SectionType


class CreateSection(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        theme = graphene.String()
        description = graphene.String()

    async def mutate(self, info: ResolveInfo, theme: str, description: str):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            section = Section(theme, description)
            await section.save(conn)
            return CreateSection(ok=True)


class Mutation(graphene.ObjectType):
    create_section = CreateSection.Field()

