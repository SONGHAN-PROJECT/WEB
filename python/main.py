import socket
import sys
from datetime import timedelta
import threading
import time
from threading import Timer

from flask_login import current_user, logout_user, LoginManager
from flask_sslify import SSLify
from flask import Flask, render_template, url_for, session, redirect, request, jsonify
from flask_oauthlib.client import OAuth

from python.DB.models.article import Article
from python.user.login_auth import login_get_info
from python.user.register import get_register
from python.user.user import User
from python.user.login import user_loader

from flask_socketio import SocketIO, emit


app = Flask(__name__, template_folder='../web', static_folder='../web/static')
socketio = SocketIO(app)
HOST = '203.250.133.111'
PORT = 8080
DEBUG = True
BUFF_SIZE = 1024
BACKLOG = 5

print('실행')
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'super_secret_key'



last_message_time = {}  # 사용자별로 마지막 메시지 시간을 저장하는 딕셔너리

@socketio.on('message')
def handle_message(data):
    user = data.get('user', 'Anonymous')
    emit('message', data, broadcast=True)
    last_message_time[user] = time.time()  # 사용자의 마지막 메시지 시간 갱신
    send_server_message_after_delay("경매가 낙찰되었습니다", 10, user)

def send_server_message_after_delay(message, delay, user):
    def delayed_message():
        time.sleep(delay)
        # 모든 사용자의 마지막 메시지 시간 중 가장 최근 시간을 찾음
        latest_time = max(last_message_time.values(), default=0)
        # 가장 최근 메시지를 보낸 사용자를 찾음
        latest_user = [k for k, v in last_message_time.items() if v == latest_time]
        if time.time() - latest_time >= delay:
            socketio.emit('server_message', {'data': f"{latest_user[0]}님, {message}"})

    threading.Thread(target=delayed_message).start()


@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/delete/<articleNo>", methods=["POST"])
def delete(articleNo):
    print(articleNo)
    article = Article.delete_article(articleNo)
    return app.response_class(response={}, status=article)

@app.route("/upload", methods=["POST"])
def upload_request():
    formdata = request.form
    post_id = formdata.get("post_id")
    title = formdata.get("title")
    start_time = formdata.get("start_time")
    description = formdata.get("description")
    image = request.files.get("image")
    user_id = formdata.get("user_id")

    status = Article.insert_article(title, description, image)
    return app.response_class(response={}, status=status)

@app.route("/index")
def index():
    return redirect(url_for('home'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("loginv2.html")

@app.route("/auth", methods=['POST', 'GET'])
def login_auth():
    return login_get_info()

@app.route("/logout", methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/chat/<articleNo>")
def chat(articleNo):
    return render_template("chat.html", article=Article.load_article_with_post_id(articleNo))

@app.route('/send_message/<articleNo>', methods=['POST'])
def send_message(articleNo):
    value = request.json["value"]
    Article.add_amount(value, articleNo)
    response_amount = Article.get_amount(articleNo)
    return jsonify({'status': 'ok', 'amount': response_amount})

@app.route("/register", methods=['POST', 'GET'])
def do_reg():
    return get_register()

@login_manager.user_loader
def load_user(user_id):
    return user_loader(user_id)

@app.route("/board")
def board():
    parameter_dict = request.args.to_dict()
    page = 1
    if "page" in parameter_dict.keys():
        page = int(parameter_dict["page"])

    if "search" in parameter_dict.keys():
        search_value = parameter_dict["search"]
        return render_template("board.html", posts=Article.search_article(search_value, page),
                               search_value=search_value,
                               page=page,
                               max_page=Article.get_max_page(search_value),)
    else:
        articles = Article.get_all_article(page)
        if articles is None:
            articles = []

        max_page = Article.get_max_page(search_value="", count=15)
        if max_page is None:
            max_page = 0

        return render_template("board.html", posts=articles, search_value="", page=0, max_page=max_page)

@app.route("/article/<articleNo>")
def article(articleNo):
    return render_template("article.html", article=Article.load_article_with_post_id(articleNo))

@app.route("/articles")
def articles():
    return {"articles": Article.load_all_article()}

if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
