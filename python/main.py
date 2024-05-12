from datetime import timedelta

from flask import Flask, render_template, url_for, session, redirect, request
from flask_oauthlib.client import OAuth

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
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route("/")
def home():
    logged_in = check_token()
    # index.html 템플릿 렌더링 시 로그인 상태 정보를 전달
    return render_template('index.html', logged_in=logged_in)

@app.route("/login")
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/check_token')
def check_token():
    return 'google_token' in session

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return '로그인 실패'

    # 로그인이 성공하면 리디렉션을 수행
    session['google_token'] = request.args.get('google_token')
    return redirect(url_for('home'))


 # 리디렉션을 처리하는 엔드포인트
# @app.route('/redirected')
# def redirected():
#     return redirect(url_for('/'))


@app.route("/board")
def board():
    logged_in = check_token()
    # index.html 템플릿 렌더링 시 로그인 상태 정보를 전달
    return render_template('board.html', logged_in=logged_in)
@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__=='__main__':
    app.run(host=HOST,port=PORT,threaded=DEBUG)