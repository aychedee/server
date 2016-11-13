
from flask import abort, render_template
from markdown import markdown
import re

from os import path, walk

from constants import SITE_URL

APP_DIR = path.dirname(path.dirname(__file__))


class Post(object):

    def __init__(self, post_url):
        self.post_url = post_url
        self.path = path.join(APP_DIR, 'posts/' + post_url) + '.md'
        if not path.exists(self.path):
            abort(404)

        self.url = post_url.split('/')[-1]
        self.author = 'Hansel'
        with open(self.path) as md:
            self.html = markdown(md.read(), extensions=['footnotes'])
        self.date = '/'.join(reversed(self.post_url.split('/')[0:3]))

    def __repr__(self):
        return 'Post("%s")' % (self.post_url,)

    def render(self):
        return render_template('post.html', post=self)

    @property
    def draft(self):
        return '::DRAFT::' in self.html

    @property
    def full_url(self):
        return SITE_URL + self.post_url

    @property
    def title(self):
        try:
            title = re.search('(?s)(?<=<h1>)(.+?)(?=</h1>)', self.html).group()
            if '</a>' in title:
                return re.search(r'(?<=>)(.+?)(?=</a>)', title).group()
            return title
        except AttributeError:
            return 'Blog'

    @classmethod
    def posts(cls, begin=None, end=None):
        files = []
        def complete_path(date_dir):
            files.extend(
                    map(lambda a: path.join(date_dir[0], a), date_dir[-1])
            )
        map(complete_path, filter(lambda a: a[-1], walk('posts')))
        posts = [p for p in [Post( f.split('/', 1)[1].rsplit('.', 1)[0]) for f in reversed(sorted(files))
            ] if not p.draft]
        if len(posts) < end:
            end = len(posts)
        return posts[begin:end], len(posts)
