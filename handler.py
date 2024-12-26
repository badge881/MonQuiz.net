from private import *  # or privateExemple
from pathlib import Path
from db import db


class Handler:
    def __init__(self) -> None:
        self.Paths = {
            '/': self._main,
            '/create': self._create,
            '/play': self._play,
        }
        self.db = db()

    def __call__(self, path: str, get: dict[str, list[str]], post: dict[str, list[str]], cookies: dict[str, str], session: dict[str, any]) -> tuple[str, list[tuple[str, str]], bytes]:
        self.GET = get
        self.POST = post
        self.COOKIES = cookies
        self.SESSION = session
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
            return self._NotFound()

    def _main(self) -> tuple[str, list[tuple[str, str]], bytes]:
        html = """<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MonQuiz.net</title>
    <link rel="icon" href="/static/images/logo.png">
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
</head>

<body lang="en">
    <header>
        <a href=" /" class="header-link">
            <img id="logo" src="/static/images/logo.png" alt="MonQuiz.net" class="header-image">
        </a>
        <nav style="display: flex; gap:20px">
            <a href="/create" class="header-link">
                Cr&eacute;er un jeu
            </a>
            <a href="/play" class="header-link">
                Rejoindre un jeu
            </a>
        </nav>
    </header>
    <main>
        <h1>Bienvenue sur MonQuiz.net</h1>
        <p>Cr&eacute;ez et jouez &agrave; des quiz en ligne gratuitement.</p>
        <p>Vous pouvez <a href="/create">cr&eacute;er</a> un quiz ou en <a href="/play">rejoindre</a> un.</p>
        <p>Les r&eacute;sultats sont enregistr&eacute;s et peuvent &ecirc;tre consult&eacute;s &agrave; tout moment.</p>
        <p>Entre amis, en famille ou a l'&eacute;cole, amusez-vous avec MonQuiz.net.</p>
    </main>
</body>

</html>"""
        return ('200 OK', [('Content-type', 'text/html')], bytes(html, 'utf-8'))

    def _create(self) -> tuple[str, list[tuple[str, str]], bytes]:
        return ('200 OK', [('Content-type', 'text/html')], bytes('Not created return on <a href="/">home</a>', 'utf-8'))

    def _play(self) -> tuple[str, list[tuple[str, str]], bytes]:
        return ('200 OK', [('Content-type', 'text/html')], bytes('Not created return on <a href="/">home</a>', 'utf-8'))

    def _NotFound(self) -> tuple[str, list[tuple[str, str]], bytes]:
        return ('404 Not Found', [('Content-type', 'text/html')], b'Not Found return on <a href="/">home</a>')
