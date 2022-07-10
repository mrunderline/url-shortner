from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

from .validation import validate_new_url
from ..utils.url import shorten_url
from ..settings import DOMAIN, DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

from ..models import Url

db.create_all()
mem_cache = {}


@app.route('/', methods=['POST'])
def new_url():
    body = request.json
    valid, data = validate_new_url(body)

    if valid is False:
        return data, 400

    original_url = data.get('url')
    shorted_url = data.get('ideal_name') or shorten_url(original_url)

    inserted, result = Url(
        original_url=original_url,
        shorted_url=shorted_url
    ).insert()
    if inserted is False:
        return result, 400

    return {
        'original_url': original_url,
        'shorted_url': DOMAIN + shorted_url
    }


@app.route('/<shorted_url>')
def resolve_original_url(shorted_url):
    if mem_cache.get(shorted_url) is None:
        url = Url().find_original_url(shorted_url=shorted_url)
        if url is None:
            return {'message': 'no url found'}, 404

        mem_cache[shorted_url] = url.original_url

    return redirect(mem_cache.get(shorted_url), 302)
