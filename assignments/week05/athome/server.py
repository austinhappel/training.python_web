import datetime
import os

# bottle
import bottle
from bottle import route, run, template, HTTPError
from bottle import static_file
from bottle import error
from beaker.middleware import SessionMiddleware

# sqlalchemy, because, why not?
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

# cork, for administration
from cork import Cork

# working directory
here = os.path.dirname(os.path.abspath(__file__))

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('admin_conf')

# init bottle? (tuts are confusing)
app = bottle.app()

# sqlalchemy setup (following tuts)
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

# install sqlalchemy plugin (following tuts)
plugin = sqlalchemy.Plugin(
    engine,  # SQLAlchemy engine created with create_engine function.
    Base.metadata,  # SQLAlchemy metadata, required only if create=True.
    keyword='db',  # Keyword used to inject session database in a route (default 'db').
    create=True,  # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True,  # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False  # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

# install sqlalchemy plugin (tuts)
app.install(plugin)

# session options for Cork / administration (tuts)
session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.cookie_expires': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.encrypt_key': 'a very random secret key!',
}

# mixin session middleware? (tuts)
app = SessionMiddleware(app, session_opts)


# # database models # #

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    title = Column(String(255))
    publish_date = Column(DateTime())
    content = Column(Text())

    # def __init__(self, title):
    #     self.title = title

    def __repr__(self):
        return "<Post('%d', '%s')>" % (self.id, self.title)


# shortener / helper methods

def postd():
    """shortener"""
    return bottle.request.forms


def post_get(name, default=''):
    """shortener"""
    return bottle.request.POST.get(name, default).strip()


def add_dummy_posts(db):
    # Add dummy posts
    post = Post(title='test title', content='lorem ipsum', publish_date=datetime.datetime.now())
    db.add(post)
    post = Post(title='another test title', content=' sldj flsk jdflksj dlfksj dflorem ipsum', publish_date=datetime.datetime.now())
    db.add(post)


# # Bottle Methods # #

# staticfiles, 404's

@route('/static/<filepath:path>')
def server_static(filepath):
    """static files"""
    static_path = here + '/static'
    return static_file(filepath, root=static_path)


@error(404)
def error404(error):
    """404 error page"""
    return 'Nothing here, sorry'


# log in / log out

@route('/login')
def login_form():
    """Serve login form"""
    return template('login_form')


@route('/login', method='POST')
def login():
    """Authenticate users"""
    username = post_get('username', '')
    password = post_get('password', '')
    aaa.login(username, password, success_redirect='/admin', fail_redirect='/login')


@route('/logout')
def logout():
    aaa.logout(success_redirect='/login')


# administrator only

@route('/admin')
def admin(db):
    """Only administrators can see this"""
    aaa.require(role='admin', fail_redirect='/login')
    posts = db.query(Post).all()

    # add 2 dummy posts if there are none.
    if len(posts) == 0:
        add_dummy_posts(db)
        posts = db.query(Post).all()

    return template('admin_page', posts=posts)


@route('/new_post', method='GET')
def new_post_form():
    """Displays a new form (admins only)"""
    aaa.require(role='admin', fail_redirect='/login')
    return template('new_post_form')


@route('/new_post', method='POST')
def new_post_create(db):
    """create a new post in the database"""
    print db
    aaa.require(role='admin', fail_redirect='/login')
    title = post_get('title', 'Blank title')
    content = post_get('content', 'No Content')
    post = Post(title=title, content=content, publish_date=datetime.datetime.now())
    db.add(post)
    bottle.redirect('/admin')


# blog post pages

@route('/post/<id:int>')
def single_post(id, db):
    post = db.query(Post).filter_by(id=id).first()
    if post:
        return template('single_post', post=post)

    return HTTPError(404)


@route('/')
def index(db):
    posts = db.query(Post).all()
    # add 2 dummy posts if there are none.
    if len(posts) == 0:
        add_dummy_posts(db)
        posts = db.query(Post).all()

    return template('index', posts=posts)


run(host='localhost', port=8080, reloader=True, quiet=False, app=app)
