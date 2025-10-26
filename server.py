from flask import Flask, render_template, request, redirect, url_for, session
from data import User, TodoList
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = "secret"


def check_user(user):
    return User().check_valid_user(user)


def check_password(user, password):
    return User().check_password(user, password)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')

        if not user or not password:
            return redirect(url_for('home'))
        if not check_user(user):
            return redirect(url_for('home'))
        if not check_password(user, password):
            return redirect(url_for('home'))

        session['username'] = user
        session['name'] = User().get_name(user)
        return redirect(url_for('index'))

    return redirect(url_for('home'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('firstname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')

        if not username or not password or not name or not confirm:
            return redirect(url_for('register'))

        if password != confirm:
            return redirect(url_for('register'))

        if check_user(username):
            return redirect(url_for('register'))

        User().create_user(user=username, name=name, password=password)
        time.sleep(1)
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/index')
def index():
    username = session.get('username')
    display_name = session.get('name')
    if not username:
        return redirect(url_for('home'))

    todo = TodoList()
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = todo.get_work(username)
    return render_template('index.html', username=display_name, current_date=today, tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    work = request.form.get('work')
    if work:
        todo = TodoList()
        todo.add_work(username, work)
    return redirect(url_for('index'))


@app.route('/complete_task', methods=['POST'])
def complete_task():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    work = request.form.get('work')
    if work:
        todo = TodoList()
        todo.done_work(username, work)
    return redirect(url_for('index'))


@app.route('/delete_task', methods=['POST'])
def delete_task():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    work = request.form.get('work')
    if work:
        todo = TodoList()
        todo.done_work(username, work)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

