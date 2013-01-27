import os
import logging

from pyramid.config import Configurator
from wsgiref.simple_server import make_server

from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


# logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

# working directory
here = os.path.dirname(os.path.abspath(__file__))


@view_config(route_name='index', renderer='templates/index.mustache')
def index_view(request):
    log.debug('index')
    data = {}

    return data


@view_config(route_name='artist', renderer='templates/artist.mustache')
def artist_view(request):
    artist_id = str(request.matchdict['id'])
    data = {
        'artist': artist_id
    }

    return data


@view_config(route_name='user', renderer='templates/user.mustache')
def user_view(request):
    user_id = str(request.matchdict['id'])
    data = {
        'user': user_id
    }
    return data


@view_config(context='pyramid.exceptions.NotFound', renderer='templates/404.mustache')
def notfound_view(self):
    return {}


if __name__ == '__main__':
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True

    # configuration setup
    config = Configurator(settings=settings)

    # add moustache renderer
    config.add_renderer(name='.mustache',
    factory='mustacherenderer.MustacheRendererFactory')

    # routes setup
    config.add_route('index', '/')
    config.add_route('artist', '/artist/{id}')
    config.add_route('user', '/user/{id}')

    # static folder setup
    config.add_static_view('static', os.path.join(here, 'static'))

    # scan for @view_config and @subscriber decorators
    config.scan()

    # serve app
    log.debug('Running server')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
