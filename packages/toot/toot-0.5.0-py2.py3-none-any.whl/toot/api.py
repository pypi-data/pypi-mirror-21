# -*- coding: utf-8 -*-

import logging
import requests

from requests import Request, Session
from future.moves.urllib.parse import quote_plus

from toot import App, User, CLIENT_NAME, CLIENT_WEBSITE

SCOPES = 'read write follow'

logger = logging.getLogger('toot')


class ApiError(Exception):
    pass


class NotFoundError(ApiError):
    pass


def _log_request(request, prepared_request):
    logger.debug(">>> \033[32m{} {}\033[0m".format(request.method, request.url))
    logger.debug(">>> DATA:    \033[33m{}\033[0m".format(request.data))
    logger.debug(">>> FILES:   \033[33m{}\033[0m".format(request.files))
    logger.debug(">>> HEADERS: \033[33m{}\033[0m".format(request.headers))


def _log_response(response):
    if response.ok:
        logger.debug("<<< \033[32m{}\033[0m".format(response))
        logger.debug("<<< \033[33m{}\033[0m".format(response.json()))
    else:
        logger.debug("<<< \033[31m{}\033[0m".format(response))
        logger.debug("<<< \033[31m{}\033[0m".format(response.content))


def _get(app, user, url, params=None):
    url = app.base_url + url
    headers = {"Authorization": "Bearer " + user.access_token}

    response = requests.get(url, params, headers=headers)
    response.raise_for_status()

    return response.json()


def _post(app, user, url, data=None, files=None):
    url = app.base_url + url
    headers = {"Authorization": "Bearer " + user.access_token}

    session = Session()
    request = Request('POST', url, headers, files, data)
    prepared_request = request.prepare()

    _log_request(request, prepared_request)

    response = session.send(prepared_request)

    _log_response(response)

    if not response.ok:
        try:
            error = response.json()['error']
        except:
            error = "Unknown error"

        if response.status_code == 404:
            raise NotFoundError(error)

        raise ApiError(error)

    response.raise_for_status()

    return response.json()


def create_app(base_url):
    url = base_url + '/api/v1/apps'

    response = requests.post(url, {
        'client_name': CLIENT_NAME,
        'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
        'scopes': SCOPES,
        'website': CLIENT_WEBSITE,
    })

    response.raise_for_status()

    data = response.json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

    return App(base_url, client_id, client_secret)


def login(app, username, password):
    url = app.base_url + '/oauth/token'

    response = requests.post(url, {
        'grant_type': 'password',
        'client_id': app.client_id,
        'client_secret': app.client_secret,
        'username': username,
        'password': password,
        'scope': SCOPES,
    })

    response.raise_for_status()

    data = response.json()
    access_token = data.get('access_token')

    return User(username, access_token)


def post_status(app, user, status, visibility='public', media_ids=None):
    return _post(app, user, '/api/v1/statuses', {
        'status': status,
        'media_ids[]': media_ids,
        'visibility': visibility,
    })


def timeline_home(app, user):
    return _get(app, user, '/api/v1/timelines/home')


def upload_media(app, user, file):
    return _post(app, user, '/api/v1/media', files={
        'file': file
    })


def search(app, user, query, resolve):
    return _get(app, user, '/api/v1/search', {
        'q': query,
        'resolve': resolve,
    })


def follow(app, user, account):
    url = '/api/v1/accounts/%d/follow' % account

    return _post(app, user, url)


def unfollow(app, user, account):
    url = '/api/v1/accounts/%d/unfollow' % account

    return _post(app, user, url)
