# flask_login에서 제공하는 사용자 클래스 객체
from flask_login import UserMixin

# DB 연결 정보가 저장되어 있는 config
import python.DB.database
import hashlib


# UserMixin 상속하여 flask_login에서 제공하는 기본 함수들 사용
class User(UserMixin):

    # User 객체에 저장할 사용자 정보
    # 그 외의 정보가 필요할 경우 추가한다. (ex. email 등)
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return str(self.user_id)

    # User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
    # 사용자가 작성한 계정 정보가 맞는지 확인하거나
    # flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.
    @staticmethod
    def get_user_info(user_id, user_pw=None):

        try:
            sql = f"SELECT user_id, username, email, password_hash, created_at, updated_at FROM users "

            if user_pw:
                user_pw = hashlib.sha256(user_pw.encode()).hexdigest()
                sql += f"WHERE username = %s AND password_hash = %s;"
                values = (user_id, user_pw)
            else:
                sql += f"WHERE user_id = '{user_id}';"
                values = (user_id, )
            result = python.DB.database.execute_query(sql, values)
            print("result : ", result)
            result[0]['result'] = 1
        except:
            result[0]['result'] = 0
        finally:
            print(result)
            return result