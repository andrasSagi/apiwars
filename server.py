from flask import Flask, jsonify, render_template, url_for, redirect, request, session
import requests
import bcrypt
import data_manager

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route('/')
@app.route('/page/<page>')
def index(page=1):
    api_result = "https://swapi.co/api/planets/?page=" + str(page)
    response = requests.get(api_result).json()
    next_page = response['next']
    previous_page = response['previous']
    planets = response['results']
    return render_template('index.html', planets=planets, page=page,
                           next_page=next_page, previous_page=previous_page,
                           session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user_password']
        data = data_manager.get_hash_by_username(username)
        if not data:
            return render_template('login.html', wrong=True)
        if verify_password(password, data['password']):
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', wrong=True)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user_name']
        taken_username = data_manager.check_username(username)
        if len(taken_username) != 0:
            return render_template('registration.html', taken_name=True)
        password = request.form['user_password']
        data_manager.register(username, hash_password(password))
        return redirect(url_for('index'))
    return render_template('registration.html')


@app.route('/vote', methods=['POST'])
def route_vote():
    user_id = data_manager.get_id_by_username(request.form['username'])['id']
    data_manager.update_vote_table(user_id, request.form['planetname'])
    return 'ok'


@app.route('/vote-statistics')
def route_vote_statistics():
    statistics = jsonify(data_manager.get_vote_statistics())
    return statistics


if __name__ == '__main__':
    app.run()
