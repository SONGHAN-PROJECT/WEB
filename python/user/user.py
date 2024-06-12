# flask_login에서 제공하는 사용자 클래스 객체
from flask_login import UserMixin

# DB 연결 정보가 저장되어 있는 config
import python.DB.database
import hashlib


def get_user_info(user_id=None, username=None, user_pw=None):
    try:
        sql = f"SELECT * FROM users "
        if user_pw:
            ser_pw = hashlib.sha256(user_pw.encode()).hexdigest()
            sql += f"WHERE username = %s AND password_hash = %s;"
            values = (username, ser_pw)
        else:
            sql += f"WHERE user_id = %s;"
            values = (user_id,)
        result = python.DB.database.execute_query(sql, values)
        print(result)
        result[0]['result'] = 1
    except:
        result[0]['result'] = 0
    finally:
        return result

class User(UserMixin):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
    def get_id(self):
        return str(self.user_id)

    def get_username(self):
        return str(self.user_name)

    # User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
    # 사용자가 작성한 계정 정보가 맞는지 확인하거나
    # flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.
