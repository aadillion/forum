import pathlib
from .schema import gqil_view


PROJECT_PATH = pathlib.Path(__file__).parent.parent


def init_routes(app, cors):
    app.router.add_route('*', '/graphiql', gqil_view, name='graphiql')