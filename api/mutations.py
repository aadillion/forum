import graphene
from graphql import ResolveInfo
from app.models import Section, Post, Comment


class CreateSection(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        theme = graphene.String()
        description = graphene.String()

    async def mutate(self, info: ResolveInfo, theme: str, description: str) -> (lambda: CreateSection):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            section = Section(theme, description)
            return CreateSection(ok=await section.save(conn))


class ChangeSection(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ = graphene.ID()
        theme = graphene.String()
        description = graphene.String()

    async def mutate(self, info: ResolveInfo, id_: int, **kwargs: dict) -> (lambda: ChangeSection):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            await Section.update(conn, {'id': id_}, kwargs)
            return CreateSection(ok=True)


class DeleteSection(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ = graphene.ID()

    async def mutate(self, info: ResolveInfo, id_: int) -> (lambda: DeleteSection):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            await Section.delete(conn, {'id': id_})
            return DeleteSection(ok=True)


class CreatePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        theme = graphene.String()
        description = graphene.String()
        section_id = graphene.Int()

    async def mutate(self, info: ResolveInfo, theme: str, description: str, section_id: int) -> (lambda: CreatePost):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            post = Post(theme, description, section_id)
            return CreatePost(ok=await post.save(conn))


class ChangePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ = graphene.ID()
        theme = graphene.String()
        description = graphene.String()

    async def mutate(self, info: ResolveInfo, id_: int, **kwargs: dict) -> (lambda: ChangePost):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            await Post.update(conn, {'id': id_}, kwargs)
            return ChangePost(ok=True)


class DeletePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ = graphene.ID()

    async def mutate(self, info: ResolveInfo, id_: int) -> (lambda: DeletePost):
        app = info.context['request'].app
        async with app['db'].acquire() as conn:
            await Post.delete(conn, {'id': id_})
            return DeletePost(ok=True)


class CreateComment(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int()
        text = graphene.String()
        parent_id = graphene.Int()

    async def mutate(self, info: ResolveInfo, **kwargs: dict) -> (lambda: CreateComment):
        app = info.context['request'].app
        post_id = kwargs.get('post_id')
        text = kwargs.get('text')
        parent_id = kwargs.get('parent_id')
        async with app['db'].acquire() as conn:
            comment = Comment(post_id, text, parent_id)
            return CreateComment(ok=await comment.save(conn))


class Mutation(graphene.ObjectType):
    create_section = CreateSection.Field()
    change_section = ChangeSection.Field()
    delete_section = DeleteSection.Field()

    create_post = CreatePost.Field()
    change_post = ChangePost.Field()
    delete_post = DeletePost.Field()

    create_comment = CreateComment.Field()
