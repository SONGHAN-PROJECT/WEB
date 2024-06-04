from flask import render_template, redirect, request, jsonify
from flask_login import logout_user, login_user
from python.user.user import User

def root():
    return redirect('/login')


def login():
    return render_template('common/template_login.html')

# 로그인 실행
# 로그인 계정 정보는 post로 받아오지만
# 일반 리소스들은 get으로 받아오므로 get과 post모두 선언해줘야 한다.
def login_get_info():
    data_from_client = request.form

    user_id = data_from_client.get('id')
    user_pw = data_from_client.get('password')

    print(user_id, user_pw)

    if user_id is None or user_pw is None:
        return jsonify({'login_success': False})

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id, user_pw)

    if user_info[0]['result'] != 0:
        print('성공')
        # 사용자 객체 생성
        login_info = User(user_id=user_info[0]['user_id'])
        # 사용자 객체를 session에 저장
        login_user(login_info)
        #클라이언트로 True값을 갖는 dictionary전송 > 클라이언트측에서 값을 받아 js로 console.log 출력
        return jsonify({'login_success': True})
    else:
        print('실패')
        return jsonify({'login_success': False})


# 로그인 실패 시 재로그인
def relogin():
    pass

# 로그아웃
def logout():
    # session 정보를 삭제한다.
    logout_user()
    return redirect('/')