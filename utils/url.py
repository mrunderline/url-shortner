import hashlib
from ..settings import SHORTNER_SALT


def shorten_url(original):
    salt = SHORTNER_SALT

    new_salt = (original + salt).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(new_salt)

    return md5.hexdigest()[-6:].replace('=', '').replace('/', '_')
