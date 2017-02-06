from datetime import datetime
from flask import session, request, render_template
from functools import partial
import re
import requests

from interpretthis.blog import Post
from interpretthis import app, constants, utilities

app.secret_key = constants.SECRET_KEY
app.logger.setLevel(constants.LOG_LEVEL)
app.logger.addHandler(constants.LOG_HANDLER)


PHOTO_DATA_URL = (
    'https://s3.amazonaws.com/'
    'photos.interpretthis.org/feed.json'
)


@app.route('/')
@utilities.cache_me(cache={})
def root():
    begin, end = int(request.args.get('begin', 0)), int(request.args.get('end', 9))
    posts, total_posts = Post.posts(begin, end)
    if end > total_posts:
        begin, end = total_posts - 10, total_posts

    render_root = partial(
        render_template, 'root.html', posts=posts, begin=end+1, end=end+11,
        at_end=end>total_posts
    )
    if 'username' in session:
        username = session['username']
        if request.remote_addr == session['address']:
            return render_root(username=username, addr=session['address'])
    return render_root()


@app.route('/feed', methods=['GET'])
def photofeed():
    response = requests.get(PHOTO_DATA_URL)
    feed = response.json()
    for photo in feed:
        photo['taken'] = datetime.strptime(photo['taken'], '%Y-%m-%d %H:%M:%S')
    return render_template(
        'photofeed.html',
        feed=feed,
        feed_json=response.content
    )


@app.route('/btsync')
def btsync():
    if 'username' in session:
        if request.remote_addr == session['address']:
            return request.get('http://localhost:8888')
    else:
        return 'Sorry'


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    app.logger.debug(request)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed, salt = utilities.get_password_hashes()[username].split(':')
        if utilities.salty_hash(password, salt) == utilities.get_password_hashes()[username]:
            session['username'] = username
            session['address'] = request.remote_addr
            return 'OK'
    return 'Failed'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return 'Passwords did not match'
        if username in utilities.get_password_hashes():
            return 'Username exists'
        with open(constants.PASSWORD_FILE, 'a') as pwdf:
            pwdf.write(constants.PWDFMT % (username, utilities.get_password_hashes(password)))
        with open('user_emails', 'a') as emailsf:
            emailsf.write(constants.PWDFMT % (username, email))
        return 'Account created for ' + username
    return 'Failed'


def post_title(html):
    try:
        return re.search('(?s)(?<=<h1>)(.+?)(?=</h1>)', html).group()
    except AttributeError:
        return 'Blog'


@app.route('/<path:post_path>')
@utilities.cache_me(cache={})
def post(post_path):
    return Post(post_path).render()


@app.route('/posts')
@utilities.cache_me(cache={})
def posts():
    return render_template('posts.html', posts=Post.posts()[0])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
