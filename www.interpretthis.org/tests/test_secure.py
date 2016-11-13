
from mock import patch
import os
import sys
import unittest

PATH = os.path.dirname(os.path.dirname(__file__))
if PATH not in sys.path:
    sys.path.append(PATH)


from interpretthis import app
from interpretthis.constants import PWDFMT
from interpretthis.utilities import salty_hash
from interpretthis.views import authenticate, root

from interpretthis.blog import Post

MOCK_PWD_LOC = 'tests/test_hashes'

MOCK_WALK_TEST_DATA = [
    ('posts', ['2100', '2013'], []),
    ('posts/2100', ['0'], []),
    ('posts/2100/0', ['0'], []),
    ('posts/2100/0/0', [], ['sad-television-treme.md', 'why-have-we-become-less-violent.md']),
    ('posts/2013', ['05'], []),
    ('posts/2013/05', ['12', '14', '13', '16'], []),
    ('posts/2013/05/12', [], ['hansel-reviews-hansel-and-gretel.md']),
    ('posts/2013/05/14', [], ['pre-pay-media-culture.md']),
    ('posts/2013/05/13', [], ['the-children-of-bitcoins.md']),
    ('posts/2013/05/16', [], ['electronic-cigarettes.md'])
]

@patch('interpretthis.constants.PASSWORD_FILE', MOCK_PWD_LOC)
class SecureTest(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(MOCK_PWD_LOC):
            os.unlink(MOCK_PWD_LOC)

    def test_root_works(self):
        with app.test_request_context('/', method='GET'):

            response = root()


    def DONTtest_authenticate_with_valid_post(self):
        print MOCK_PWD_LOC
        with open(MOCK_PWD_LOC, 'a') as f:
            f.write(PWDFMT % ('douglas', salty_hash('tribble')))
            f.write(PWDFMT % ('dave', salty_hash('tribble')))

        data = dict(username='douglas', password='tribble')
        with app.test_request_context('/authenticate', method='POST', data=data):

            response = authenticate()

            self.assertEqual(response, 'OK')


class BlogTest(unittest.TestCase):

    @patch('interpretthis.blog.walk')
    def test_posts_classmethod(self, mock_walk):

        mock_walk.return_value = MOCK_WALK_TEST_DATA

        posts, total_posts = Post.posts()

        print [p for p in posts],

        self.assertEqual(
            [repr(p) for p in posts],
            [
                'Post("2013/05/16/electronic-cigarettes")',
                'Post("2013/05/14/pre-pay-media-culture")',
                'Post("2013/05/13/the-children-of-bitcoins")',
                'Post("2013/05/12/hansel-reviews-hansel-and-gretel")'
            ]
        )
        self.assertEqual(total_posts, 4)



if __name__ == '__main__':
    unittest.main()
