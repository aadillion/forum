import graphene
import asyncio
from graphql.execution.executors.asyncio import AsyncioExecutor
from aiohttp_graphql import GraphQLView
from api.queries import Query
from api.mutations import Mutation


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)

gqil_view = GraphQLView(
    schema=schema,
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=True,
    enable_async=True,
)

gql_view = GraphQLView(
    schema=schema,
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=False,
    enable_async=True,
)