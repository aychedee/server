
import hashlib
import random
import string


PASSWORD_HASHES = {}
PASSWORD_FILE = 'hashed_passwords'
PWDFMT = '%s %s\n'
NOT_CACHING = True

def cache_me(cache):
    def wrapper(func):
        if NOT_CACHING:
            return func
        def inner(*args, **kwargs):
            hashed_kwargs = hash(frozenset(kwargs.items()))
            try:
                cached_response = cache[(args, hashed_kwargs)]
                return cached_response
            except KeyError:
                cache[(args, hashed_kwargs)] = func(*args, **kwargs)
                return cache[(args, hashed_kwargs)]

        return inner
    return wrapper

def salty_hash(password, salt=None):
    if not salt:
        salt = ''.join(random.choice(string.ascii_uppercase) for x in range(6))
    hashed = hashlib.sha256(password + salt).hexdigest()
    return hashed + ':' + salt

def get_password_hashes():
    if len(PASSWORD_HASHES) == 0:
        with open(PASSWORD_FILE) as f:
            for line in f.readlines():
                username, hashed = line.split()
                PASSWORD_HASHES[username] = hashed
                return PASSWORD_HASHES
    return PASSWORD_HASHES



