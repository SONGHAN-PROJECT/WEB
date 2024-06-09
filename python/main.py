import socket
import sys
from datetime import timedelta

from flask_login import current_user, logout_user, login_manager, LoginManager
from flask_sslify import SSLify
from flask import Flask, render_template, url_for, session, redirect, request, jsonify
from flask_oauthlib.client import OAuth

from python.DB.models.article import Article
from python.user.login_auth import login_get_info
from python.user.register import get_register
from python.user.user import User

app = Flask(__name__, template_folder='../web', static_folder='../web/static')

HOST = '203.250.133.111'
PORT = 8080
DEBUG = True
BUFF_SIZE=1024
BACKLOG=5

# conn_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# conn_sock.setblocking(0)
# conn_sock.bind((HOST,PORT))
# conn_sock.listen(BACKLOG)
# rd_list, wr_list, err_list = [sys.stdin, conn_sock],[],[]

print('실행')
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'super_secret_key'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
# app.secret_key = 'your_secret_key_here'
# oauth = OAuth(app)
# google = oauth.remote_app(
#     'google',
#     consumer_key='947304049541-4atb6apclsjndp4euaq4ku8sk98hj2bh.apps.googleusercontent.com',
#     consumer_secret='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',
#     request_token_params={
#         'scope': 'email',
#     },
#     base_url='https://www.googleapis.com/oauth2/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='http://accounts.google.com/o/oauth2/token',
#     authorize_url='http://localhost:8080/login/authorized',
# )

@app.route("/upload")
def upload():
    return render_template("upload.html")
# , logged_in=logged_in

@app.route("/delete/<articleNo>", methods = ["POST"])
def delete(articleNo):
    print(articleNo)
    article = Article.delete_article(articleNo)
    return app.response_class(response={}, status = article)

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
    # index.html 템플릿 렌더링 시 로그인 상태 정보를 전달
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("loginv2.html")

@app.route("/auth", methods=['POST', 'GET'])
def login_auth():
    return login_get_info()


@app.route("/logout",methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/chat/<articleNo>")
def chat(articleNo):
    return render_template("chat.html",article=Article.load_article_with_post_id(articleNo))

@app.route('/send_message/<articleNo>', methods=['POST'])
def send_message(articleNo):
    value = request.json["value"]
    Article.add_amount(value, articleNo)
    response_amount=Article.get_amount(articleNo)
    return jsonify({'status': 'ok', 'amount': response_amount})

@app.route("/register", methods=['POST', 'GET'])
def do_reg():
    return get_register()

@login_manager.user_loader
def load_user(user_id):
	return User(user_id)

# @app.route('/check_token')
# def check_token():
#     return 'google_token' in session

# @app.route('/login/authorized')
# def authorized():
#     resp = google.authorized_response()
#     if resp is None or resp.get('access_token') is None:
#         print('실패',resp)
#         return '로그인 실패'
#
#     # 로그인이 성공하면 리디렉션을 수행
#     print('성공')
#     session['google_token'] = (resp['access_token'], '')
#     return redirect(url_for('home'))


 # 리디렉션을 처리하는 엔드포인트
# @app.route('/redirected')
# def redirected():
#     return redirect(url_for('/'))


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
        # get_all_article 메서드 호출
        articles = Article.get_all_article(page)
        if articles is None:
            articles = []

        # get_max_page 메서드 호출
        max_page = Article.get_max_page(search_value="", count=15)
        if max_page is None:
            max_page = 0

        # render_template 호출
        return render_template("board.html", posts=articles, search_value="", page=0, max_page=max_page)


@app.route("/article/<articleNo>")
def article(articleNo):
    return render_template("article.html", article=Article.load_article_with_post_id(articleNo))

@app.route("/articles")
def articles():
    return {"articles": Article.load_all_article()}



if __name__=='__main__':
    app.run(host=HOST,port=PORT,threaded=DEBUG)