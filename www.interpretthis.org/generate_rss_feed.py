from datetime import datetime
import PyRSS2Gen
import sys
from os import path

sys.path.append(path.dirname(__file__))

from interpretthis import constants
from interpretthis.blog import Post

items = [
        PyRSS2Gen.RSSItem(
            title=p.title,
            link=p.full_url,
            description=p.html,
            guid=PyRSS2Gen.Guid(p.full_url),
            pubDate=datetime.strptime(p.date, '%d/%m/%Y')
        )
                for p in Post.posts()[0]
        ]



rss = PyRSS2Gen.RSS2(
        title='Interprethis :: Posts',
        link=constants.SITE_URL,
        description='Interprethis is the personal blog of Hansel Dunlop',

        lastBuildDate=datetime.utcnow(),

        items=items
 )
print 'Generated feed for', str(len(items)), 'items'
rss.write_xml(open('rss/interpretthis_rss.xml', 'w'))

