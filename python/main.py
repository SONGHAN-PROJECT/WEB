from datetime import timedelta
from flask_sslify import SSLify
from flask import Flask, render_template, url_for, session, redirect, request
from flask_oauthlib.client import OAuth

from python.DB.models.article import Article

app = Flask(__name__, template_folder='../web', static_folder='../web/static')

HOST = 'localhost'
PORT = 8080
DEBUG = True

print('실행')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.secret_key = 'your_secret_key_here'
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='947304049541-4atb6apclsjndp4euaq4ku8sk98hj2bh.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='http://accounts.google.com/o/oauth2/token',
    authorize_url='http://localhost:8080/login/authorized',
)
@app.route("/index")
def index():
    return redirect(url_for('home'))
@app.route("/")
def home():
    logged_in = check_token()
    print(logged_in)
    # index.html 템플릿 렌더링 시 로그인 상태 정보를 전달
    return render_template('index.html', logged_in=logged_in)

@app.route("/login")
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    # 세션을 비움
    session.pop('google_token', None)
    # 로그아웃 후 어떤 페이지로 리디렉션할지 설정
    return redirect(url_for('home'))

@app.route('/check_token')
def check_token():
    return 'google_token' in session

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        print('실패',resp)
        return '로그인 실패'

    # 로그인이 성공하면 리디렉션을 수행
    print('성공')
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('home'))


 # 리디렉션을 처리하는 엔드포인트
# @app.route('/redirected')
# def redirected():
#     return redirect(url_for('/'))


@app.route("/board")
def board():
    logged_in = check_token()
    parameter_dict = request.args.to_dict()
    page = 1
    if "page" in parameter_dict.keys():
        page = int(parameter_dict["page"])

    if "search" in parameter_dict.keys():
        search_value = parameter_dict["search"]
        return render_template("board.html", posts=Article.search_article(search_value, page),
                               search_value=search_value,
                               page=page,
                               max_page=Article.get_max_page(search_value),
                               logged_in=logged_in)

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
        return render_template("board.html", posts=articles, search_value="", page=0, max_page=max_page, logged_in=logged_in)


@app.route("/article/<articleNo>")
def article(articleNo):
    return render_template("article.html", article=Article.load_article_with_post_id(articleNo))

@app.route("/articles")
def articles():
    return {"articles": Article.load_all_article()}



if __name__=='__main__':
    ssl_cert = 'C:\pycharm\WEB\web\server.crt'
    ssl_key = 'C:\pycharm\WEB\web\server.key'
    app.run(host=HOST,port=PORT,threaded=DEBUG)