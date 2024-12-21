from private import *  # or privateExemple
from pathlib import Path


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
        elif path.startswith('/static/'):
            path: Path = Path(ServerDirectory + path)
            match path.suffix:
                case '.css':
                    return ('200 OK', [('Content-type', 'text/css')], path.read_bytes())
                case '.html':
                    return ('200 OK', [('Content-type', 'text/html')], path.read_bytes())
                case '.js':
                    return ('200 OK', [('Content-type', 'text/js')], path.read_bytes())
                case '.png':
                    return ('200 OK', [('Content-type', 'image/png')], path.read_bytes())
                case '.jpg':
                    return ('200 OK', [('Content-type', 'image/jpg')], path.read_bytes())
                case '.jpeg':
                    return ('200 OK', [('Content-type', 'image/jpeg')], path.read_bytes())
                case '.gif':
                    return ('200 OK', [('Content-type', 'image/gif')], path.read_bytes())
                case '.svg':
                    return ('200 OK', [('Content-type', 'image/svg')], path.read_bytes())
                case '.ico':
                    return ('200 OK', [('Content-type', 'image/ico')], path.read_bytes())
                case _:
                    return ('200 OK', [('Content-type', 'text/plain')], path.read_bytes())
        else:
            return self.NotFound()

    def main(self):
        return ('200 OK', [('Content-type', 'text/plain')], b'Hello World')

    def NotFound(self):
        return ('404 Not Found', [('Content-type', 'text/plain')], b'Not Found')
