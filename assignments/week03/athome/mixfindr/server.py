import os
import logging
import urllib2
import urllib
import json
import types
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

# last.fm base url
last_fm_base_url = 'http://ws.audioscrobbler.com/2.0/'
last_fm_api_key = str(os.environ.get('last_fm_api_key'))


@view_config(route_name='index', renderer='templates/index.mustache')
def index_view(request):
    data = {}

    return data


@view_config(route_name='artist', renderer='templates/artist.mustache')
def artist_view(request):
    artist_id = str(request.matchdict['id'])
    url_similar_artists = '%s?method=artist.getsimilar&%s&format=json' % (last_fm_base_url, urllib.urlencode({'artist': artist_id, 'api_key': last_fm_api_key}))
    req_similar_artists = urllib2.urlopen(url_similar_artists)
    similar_artists = json.loads(req_similar_artists.read())

    similar_artists_names = []
    log.debug(similar_artists)
    log.debug(type(similar_artists['similarartists']['artist']))
    log.debug(isinstance(similar_artists['similarartists']['artist'], types.DictionaryType))

    if similar_artists['similarartists'] != None and\
    isinstance(similar_artists['similarartists']['artist'], types.ListType):
        for x in similar_artists['similarartists']['artist'][0:5]:
            similar_artists_names.append(x['name'])

    data = {
        'artist': artist_id,
        'similar_artists_names': similar_artists_names,
        'json': json.dumps(similar_artists['similarartists']['artist'][0:5], indent=4)
    }

    return data


@view_config(route_name='user', renderer='templates/user.mustache')
def user_view(request):
    user_id = str(request.matchdict['id'])
    url_user_top_artists = '%s?method=user.gettopartists&%s&format=json' % (last_fm_base_url, urllib.urlencode({'user': user_id, 'api_key': last_fm_api_key}))
    req_user_top_artists = urllib2.urlopen(url_user_top_artists)
    user_top_artists = json.loads(req_user_top_artists.read())
    user_top_artists_names = []

    for x in user_top_artists['topartists']['artist'][0:5]:
        log.debug(x)
        user_top_artists_names.append({
            'name': x['name'],
            'url': urllib2.quote(x['name'].encode('unicode-escape'))
        })
    data = {
        'user': user_id,
        'json': json.dumps(user_top_artists, indent=4),
        'user_top_artists_names': user_top_artists_names
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
