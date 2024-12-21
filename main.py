from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
from expiringdict import ExpiringDict
from http.cookies import _unquote as unquote
from random import choice
from private import *  # or privateExemple
from handler import Handler

AllPeopleSession = ExpiringDict(
    max_len=200, max_age_seconds=21600)


def getHexString() -> str:
    while True:
        if not AllPeopleSession.get(i := ''.join([choice('0123456789abcdef') for _ in range(32)])):
            return i


def application(environ, start_response):
    global AllPeopleSession
    Post: dict[str, list[str]] = {}
    Get: dict[str, list[str]] = {}
    Cookies: dict[str, str] = {}
    RequestedPath = environ["PATH_INFO"]

    # POST dict:
    if True:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        for k, v in parse_qs(request_body).items():
            Post[escape(str(k, "utf-8"))] = [escape(str(i, "utf-8"))
                                             for i in v]

    # GET dict
    if True:
        for k, v in parse_qs(environ['QUERY_STRING']).items():
            Get[escape(k)] = [escape(i) for i in v]

    # COOKIES dict
    if True:
        for chunk in environ.get("HTTP_COOKIE", "").split(";"):
            if "=" in chunk:
                key, val = chunk.split("=", 1)
            else:
                key, val = "", chunk
            key, val = key.strip(), val.strip()
            if key or val:  # valid Cookie
                Cookies[key] = unquote(val)

    # SESSION dict
    if True:
        if not Cookies.get("session"):
            Cookies['session'] = getHexString()
            nbSessionPeople += 1
        if not AllPeopleSession.get(Cookies["session"], None):
            AllPeopleSession[Cookies["session"]] = {}

    status, response_headers, response_body = Handler(
        Get, Post, Cookies, AllPeopleSession[Cookies["session"]])(RequestedPath)

    start_response(status, response_headers)
    return [response_body]


if __name__ == "__main__":
    httpd = make_server('0.0.0.0', 80, application)
    httpd.serve_forever(0.1)
