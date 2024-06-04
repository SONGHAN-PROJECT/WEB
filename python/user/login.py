import user

def user_loader(user_id):
    # 사용자 정보 조회
    user_info = user.User.get_user_info(user_id)
    # user_loader함수 반환값은 사용자 '객체'여야 한다.
    # 결과값이 dict이므로 객체를 새로 생성한다.
    login_info = user.User(user_id=user_info['user_id'])

    return login_info
    #사용자 객체 생성완료

# login_required로 요청된 기능에서 현재 사용자가 로그인되어 있지 않은 경우
# unauthorized 함수를 실행한다.
# @login_manager.unauthorized_handler
# def unauthorized():
#     # 로그인되어 있지 않은 사용자일 경우 첫화면으로 이동
#     return redirect("/")