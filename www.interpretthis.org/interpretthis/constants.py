# Constants for interpretthis.org

import logging
from os import path

SITE_NAME = 'interpretthis.org'
SITE_URL = 'http://www.' + SITE_NAME + '/'
SECRET_KEY = '\xccb\x02\xbe\x87"\x7f\xaf\xeeq3\xac\xd3=\xb0n\xd1\xfcm\x80B'
LOG_FILE = '/var/log/interpretthis.org.log'
LOG_HANDLER = logging.FileHandler(LOG_FILE)
LOG_LEVEL = logging.DEBUG
APP_DIR = path.dirname(path.dirname(__file__))
PASSWORD_HASHES = {}
PASSWORD_FILE = 'hashed_passwords'
PWDFMT = '%s %s\n'
NOT_CACHING = True

