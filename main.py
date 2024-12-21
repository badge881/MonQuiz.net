from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
from hashlib import sha256
from expiringdict import ExpiringDict


def set_cookie_header(name, value):
    return ('Set-Cookie', '{}={}'.format(name, value))


AllPeopleSession: ExpiringDict = ExpiringDict(
    max_len=200, max_age_seconds=21600)
nbSessionPeople: int = 1


def application(environ, start_response):
    global nbSessionPeople, AllPeopleSession
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
        cookie_header: str = environ.get('HTTP_COOKIE', '')
        if cookie_header:
            for cookie in cookie_header.split(';'):
                key, value = cookie.strip().split('=', 1)
                Cookies[key] = value

    # SESSION dict
    if True:
        if not Cookies.get("session", ""):
            Cookies['session'] = sha256(
                bytes(str(nbSessionPeople), "utf-8")).hexdigest()
            nbSessionPeople += 1
        if not AllPeopleSession.get(Cookies["session"], None):
            AllPeopleSession[Cookies["session"]] = {}

    status, response_headers, response_body = Handler(
        Get, Post, Cookies, AllPeopleSession[Cookies["session"]])(RequestedPath)

    start_response(status, response_headers)
    return [response_body]


class Handler:
    def __init__(self, get: dict[str, list[str]], post: dict[str, list[str]], cookies: dict[str, str], session: dict[str, any]):
        self.GET = get
        self.POST = post
        self.COOKIES = cookies
        self.SESSION = session
        self.Paths = {
            '/': self.main,
        }

    def __call__(self, path: str):
        if path in self.Paths:
            return self.Paths[path]()
        else:
            return self.NotFound()

    def main(self):
        return ('200 OK', [('Content-type', 'text/plain')], b'Hello World')

    def NotFound(self):
        return ('404 Not Found', [('Content-type', 'text/plain')], b'Not Found')


if __name__ == "__main__":
    httpd = make_server('0.0.0.0', 80, application)
    httpd.serve_forever(0.1)
