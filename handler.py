from private import *  # or privateExemple
from globalFunctions import *
from pathlib import Path
from db import db


class Handler:
    def __init__(self) -> None:
        self.Paths = {
            '/': self._main,
            '/create': self._create,
            '/play': self._play,
            '/login': self._login
        }
        self.db = db("db.db")

    def __call__(self, path: str, get: dict[str, list[str]], post: dict[str, list[str]], cookies: dict[str, str], session: list[dict[str, any]]) -> tuple[str, list[tuple[str, str]], bytes]:
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

<body lang="fr">
    <header>
        <a href=" /" class="header-link">
            <img id="logo" src="/static/images/logo.png" alt="MonQuiz.net" class="header-image">
        </a>
        <nav style="display: flex;gap:20px">
            <a href="/create" class="header-link">
                Créer un jeu
            </a>
            <a href="/play" class="header-link">
                Rejoindre un jeu
            </a>
            {login_logout}
        </nav>
    </header>
    <main>
        <h1>Bienvenue sur MonQuiz.net</h1>
        <p>Créez et jouez &agrave;des quiz en ligne gratuitement.</p>
        <p>Vous pouvez <a href="/create">créer</a> un quiz ou en <a href="/play">rejoindre</a> un.</p>
        <p>Les résultats sont enregistrés et peuvent &ecirc;tre consultés &agrave;tout moment.</p>
        <p>Entre amis, en famille ou a l'école, amusez-vous avec MonQuiz.net.</p>
    </main>
</body>

</html>"""

        if not self.SESSION[0].get("userId"):
            login_logout = """<a href="/login" class="header-link">
    Se connecter
</a>"""
        else:
            login_logout = """<a href="/logout" class="header-link">
    Se deconnecter
</a>"""

        html = html.format(login_logout=login_logout)
        return ('200 OK', [('Content-type', 'text/html')], bytes(html, 'utf-8'))

    def _create(self) -> tuple[str, list[tuple[str, str]], bytes]:
        html = """<!DOCTYPE html>
<html>

<head>
    <meta charset = "UTF-8">
    <meta name = "viewport" content = "width=device-width, initial-scale=1.0">
    <title> MonQuiz.net </title>
    <link rel = "icon" href = "/static/images/logo.png">
    <link rel = "stylesheet" type = "text/css" href = "/static/css/main.css">
</head>

<body lang = "en">
    <header>
        <a href = "/" class = "header-link">
            <img id = "logo" src = "/static/images/logo.png" alt = "MonQuiz.net" class = "header-image">
        </a>
        <nav style = "display: flex;gap:20px">
            <a href = "/create" class = "header-link">
                Créer un jeu
            </a>
            <a href = "/play" class = "header-link">
                Rejoindre un jeu
            </a>
            {login_logout}
        </nav>
    </header>
    <main>
        {Comment1}
        <h1> Créer un quiz </h1>
        <form action = "/create" method = "post">
            <label for = "quiz-name"> Nom du quiz </label>
            <input type = "text" id = "quiz-name" name = "quiz-name" required>
            <label for = "quiz-description"> Description </label>
            <textarea id = "quiz-description" name = "quiz-description" required> </textarea>
            <label for = "quiz-questions"> Questions </label>
            <input type = "number" id = "quiz-questions" name = "quiz-questions" required>
            <button type = "submit"> Créer </button>
        </form>
        <h1> Quiz créés </h1>
        {quizs}
        {Comment2}
    </main>
</body>
</html> """

        if not self.SESSION[0].get("userId"):
            login_logout = """ <a href = "/login" class = "header-link">
    Se connecter
</a> """
            comment1 = "<!--"
            comment2 = "--> <h1>Erreur</h1><p>Vous avez besoin d'être connecter pour créer un quiz</p>"
            quizs = ""
        else:
            login_logout = """ <a href = "/logout" class = "header-link">
    Se deconnecter
</a>"""
            comment1 = ""
            comment2 = ""
            Dbquizs = self.db.execute("SELECT id, title FROM quizzes WHERE authorId = ?", (self.SESSION[0].get("userId"),))
            if Dbquizs == []:
                quizs = "Vous n'avez pas de quizs"
            else:
                pass

        html = html.format(**{"login_logout": login_logout, "Comment1": comment1,
                              "Comment2": comment2, "quizs": quizs})

        return ('200 OK', [('Content-type', 'text/html')], bytes(html, 'utf-8'))

    def _play(self) -> tuple[str, list[tuple[str, str]], bytes]:
        return ('200 OK', [('Content-type', 'text/html')], bytes('Not created return on <a href="/">home</a>', 'utf-8'))

    def _login(self) -> tuple[str, list[tuple[str, str]], bytes]:
        html = """<!DOCTYPE html>
<html>

<head>
    <meta charset = "UTF-8">
    <meta name = "viewport" content = "width=device-width, initial-scale=1.0">
    <title> MonQuiz.net </title>
    <link rel = "icon" href = "/static/images/logo.png">
    <link rel = "stylesheet" type = "text/css" href = "/static/css/main.css">
</head>

<body lang = "en">
    <header>
        <a href = "/" class = "header-link">
            <img id = "logo" src = "/static/images/logo.png" alt = "MonQuiz.net" class = "header-image">
        </a>
        <nav style = "display: flex;gap:20px">
            <a href = "/create" class = "header-link">
                Créer un jeu
            </a>
            <a href = "/play" class = "header-link">
                Rejoindre un jeu
            </a>
        </nav>
    </header>
    <main>
        {notifs}
        <div style="text-align: center; border: 2px; margin: 10px">
            <form action="/login" method="post">
                <label for="email">Votre address mail</label>
                    <input type="email" id="email" name="email" placeholder="example@email.com" required><br>
                <label for="password">Votre mot de passe</label>
                    <input type="password" id="password" name="password" required><br>
                <input type="submit" value="Se connecter">
            </form>
            Vous n'avez pas encore de compte ? <a href="/singup">En crée un</a>
        </div>
    </main>
</body>
</html> """
        print((self.POST.get("email") is not None) and (self.POST.get("password")[0] is not None))
        if self.POST.get("email") is not None and self.POST.get("password") is not None and (liste := self.db.execute("SELECT id, password FROM users WHERE email = ?", (self.POST.get("email")[0],))) != [] and self.POST.get("password")[0] == liste[0][1]:
            self.SESSION[0]["userId"] = liste[0][0]
        elif self.POST.get("email") is not None and self.POST.get("password")is not None:
            html = html.format(
                notifs="<div><h2>Erreur de connection</h2>combinaison email, mot de passe invalide</div>")
        else:
            html = html.format(notifs="")

        if self.SESSION[0].get("userId") is not None:
            html = 'You will be redirected on <a href="/">home</a> if it\'s not working click on the link<script>window.location.replace("/");</script>'
        return ("200 OK", [('Content-type', 'text/html')], bytes(html, 'utf-8'))

    def _NotFound(self) -> tuple[str, list[tuple[str, str]], bytes]:
        return ('404 Not Found', [('Content-type', 'text/html')], b'Not Found return on <a href="/">home</a>')
