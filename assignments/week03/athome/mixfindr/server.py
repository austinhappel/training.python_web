import os
import logging
import urllib2
import urllib
import json
import types
from pyramid.config import Configurator
from wsgiref.simple_server import make_server

# from pyramid.exceptions import NotFound
# from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


# logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

# working directory
here = os.path.dirname(os.path.abspath(__file__))

# api base url's
last_fm_base_url = 'http://ws.audioscrobbler.com/2.0/'
last_fm_api_key = str(os.environ.get('last_fm_api_key'))
mixcloud_base_url = 'http://api.mixcloud.com/'


# find mixes using mixcloud api
def find_artist_mixes(artist_id):
    query = {
        'q': artist_id.encode('utf-8'),
        'type': 'cloudcast',
        'limit': '5'
    }
    url_artist_mixes = '%ssearch/?%s' % (mixcloud_base_url, urllib.urlencode(query))
    req_artist_mixes = urllib2.urlopen(url_artist_mixes)
    artist_mixes = json.loads(req_artist_mixes.read())
    return artist_mixes


def get_and_filter_artist_mixes(artist_id):
    artist_mixes = find_artist_mixes(artist_id)
    filtered_artist_mixes = []

    # filter out just the name and url of found mixcloud mixes
    for mix in artist_mixes['data']:
        filtered_artist_mixes.append({
            'url': mix['url'],
            'title': mix['name']
            })

    return filtered_artist_mixes


# find similar artists using last.fm api
def find_similar_artists(artist_id):
    url_similar_artists = '%s?method=artist.getsimilar&%s&format=json' % (last_fm_base_url, urllib.urlencode({'artist': artist_id.encode('utf-8'), 'api_key': last_fm_api_key}))
    req_similar_artists = urllib2.urlopen(url_similar_artists)
    similar_artists = json.loads(req_similar_artists.read())
    return similar_artists


# get user's top artists from last.fm
def get_user_top_artists(user_id):
    url_user_top_artists = '%s?method=user.gettopartists&%s&format=json' % (last_fm_base_url, urllib.urlencode({'user': user_id, 'api_key': last_fm_api_key}))
    req_user_top_artists = urllib2.urlopen(url_user_top_artists)
    user_top_artists = json.loads(req_user_top_artists.read())
    return user_top_artists


# url: /
@view_config(route_name='index', renderer='templates/index.mustache')
def index_view(request):
    data = {}
    return data


# url: /artist/:id
@view_config(route_name='artist', renderer='templates/artist.mustache')
def artist_view(request):
    artist_id = request.matchdict['id']
    similar_artists = find_similar_artists(artist_id)
    artist_mixes = find_artist_mixes(artist_id)

    filtered_artist_mixes = []

    # filter out just the name and url of found mixcloud mixes
    for mix in artist_mixes['data']:
        filtered_artist_mixes.append({
            'url': mix['url'],
            'title': mix['name']
            })

    # filter out the names of similar artists from the last.fm data for display
    similar_artists_links = []

    # last.fm api returns array if there are similar artists, or a string if there
    # are none. Need to check for this.
    if hasattr(similar_artists, 'similarartists') and\
    isinstance(similar_artists['similarartists']['artist'], types.ListType):
        for x in similar_artists['similarartists']['artist'][0:5]:
            similar_artists_links.append({
                'name': x['name'].encode('ascii', 'xmlcharrefreplace'),
                'url': '/artist/' + x['name']
                })

    data = {
        'artist': artist_id.encode('ascii', 'xmlcharrefreplace'),
        'similar_artists_links': similar_artists_links,
        'json': json.dumps(artist_mixes, indent=4),
        'filtered_artist_mixes': filtered_artist_mixes
    }

    return data


# url: /user/:id
@view_config(route_name='user', renderer='templates/user.mustache')
def user_view(request):
    user_id = str(request.matchdict['id'])
    user_top_artists = get_user_top_artists(user_id)
    user_top_artists_data = [[]]

    # loop through the top 6 artists
    # create links for artists
    # get mixcloud mixes
    # create rows with sets of 3 artists
    count = 0
    row = 0
    for x in user_top_artists['topartists']['artist'][0:6]:
        log.debug(row)
        user_top_artists_data[row].append({
            'name': x['name'],
            'url': urllib2.quote(x['name'].encode('utf-8')),
            'mixes': get_and_filter_artist_mixes(x['name'])
        })

        count += 1
        if (count % 3 == 0):
            row += 1
            user_top_artists_data.append([])

    data = {
        'user': user_id,
        'json': json.dumps(user_top_artists, indent=4),
        'user_top_artists_data': user_top_artists_data
    }

    return data


# url: /api/artist/:id
@view_config(route_name='api_artist', renderer='json')
def api_artist_view(request):
    artist_id = str(request.matchdict['id'])
    artist_mixes = get_and_filter_artist_mixes(artist_id)
    return artist_mixes


# 404
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
    config.add_route('api_artist', '/api/artist/{id}')
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
