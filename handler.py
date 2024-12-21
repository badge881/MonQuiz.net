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
