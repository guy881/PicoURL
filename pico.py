from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
from werkzeug.debug import DebuggedApplication
app_url = 'http://127.0.0.1:5000/'
app = Flask(__name__)
app.secret_key = 'P^&X!123-><xD+RRRR^^'
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
linkbase = {}


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        zalogowano = "Zaloguj"
        if 'username' in session:
            zalogowano = "Wyloguj " + session['username']
            return render_template('index_logged.html', zalogowano=zalogowano)
        return render_template('index.html', zalogowano=zalogowano)
    if request.method == 'POST':
        url = request.form['url']
        uuid = uuid4().__str__()
        shortUrl = str(uuid)[:6]
        linkbase[shortUrl] = url
        return render_template('link_created.html', shortUrl=shortUrl)


@app.route('/<url>')
def redir(url):
    print url
    return redirect(linkbase[url], 301)


@app.route('/link')
def link():
    if 'username' in session:
        return render_template('linki.html', linkbase=linkbase)
    return redirect(app_url)


@app.route( '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            del session['username']
            return redirect(app_url)
        return render_template('login_form.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'pawel' and password == 'pawel':
            session['username'] = username
            return redirect(app_url)
        return render_template('login_failure.html', username=username)


if __name__ == '__main__':
    app.run()
