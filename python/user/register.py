import python.DB.database # DB 연결 정보가 저장되어 있는 config
from flask import request, jsonify
import re
import hashlib

def get_register():
    # 데이터 옮겨받는 과정 추가할것 register.html에 전송과정추가해야함
    data_form_client = request.form
    identifier = data_form_client.get('reg_id')
    password = data_form_client.get('reg_password')
    password = hashlib.sha256(password.encode()).hexdigest()
    email = data_form_client.get('reg_email')

    # 아이디에 영어, 숫자만 있는지 확인하는 정규표현식 생성
    identifier_pattern = re.compile(f'^[a-zA-Z0-9-.]+$')

    if not identifier_pattern.match(identifier): # 정규표현식에 맞지 않을때
        return jsonify({'register_type': -2, 'register_message': "올바른 아이디 형식이 아닙니다."})

    # 이메일 형식이 맞는지 확인하는 정규표현식 생성
    email_pattern = re.compile(f'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(email): # 정규표현식에 맞지 않을때
        return jsonify({'register_type': -2, 'register_message': "올바른 이메일 주소 형식이 아닙니다."})

    try:
        exists_id_sql = "SELECT * FROM users WHERE username=%s;"
        exists_id_value = (identifier, )
        exists_id_result = python.DB.database.execute_query(exists_id_sql, exists_id_value)

        if exists_id_result:
            # 이미 있는 아이디인 경우
            return jsonify({'register_type': -3, 'register_message': "이미 사용 중인 아이디입니다."})


        exists_email_sql = "SELECT * FROM users WHERE email=%s;"
        exists_email_value = (email, )
        exists_email_result = python.DB.database.execute_query(exists_email_sql, exists_email_value)

        if exists_email_result:
            # 이미 있는 이메일인 경우
            return jsonify({'register_type': -4, 'register_message': "이미 사용 중인 이메일입니다."})

        insert_sql = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s);"
        insert_values = (identifier, password, email)
        python.DB.database.execute_query(insert_sql, insert_values)

        return jsonify({'register_type': 1, 'register_message': "회원가입 성공!"})
        #회원가입 성공 페이지+로그인화면으로 돌려보내기
    except Exception as e:
        print("error : ", e)
        #회원가입 실패 페이지 ('입력정보를 확인해주세요') + 회원가입페이지 새로고침
        return jsonify({'register_type': 0, 'register_message': "회원가입 중 오류가 발생했습니다!"})